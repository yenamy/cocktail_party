import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Copy, RefreshCw, Sparkles, Martini } from "lucide-react";

// -----------------------------
// 데이터 모델
// -----------------------------
type Unit = "ml" | "piece" | "leaf" | "g" | "wedge";

type Ingredient = {
  name: string;
  amount: number;
  unit: Unit;
  note?: string;
  range?: [number, number]; // e.g., 토닉 90~120
};

type Recipe = {
  id: string;
  name: string;
  tagline: string;
  color: string; // UI 테마 색상
  ingredients: Ingredient[];
  howto?: string[]; // 간단 빌드 가이드
};

const RECIPES: Recipe[] = [
  {
    id: "mojito",
    name: "모히또",
    tagline: "민트 향 터지는 섬 한 잔!",
    color: "#10b981",
    ingredients: [
      { name: "럼", amount: 45, unit: "ml" },
      { name: "라임", amount: 0.5, unit: "piece", note: "즙 + 조각" },
      { name: "민트", amount: 7, unit: "leaf" },
      { name: "설탕/시럽", amount: 10, unit: "ml" },
      { name: "토닉", amount: 105, unit: "ml", range: [90, 120] },
    ],
    howto: [
      "잔에 라임즙·시럽·민트를 넣고 살살 빻기",
      "얼음 가득 → 럼 → 토닉",
      "바스푼으로 1–2회 가볍게 스터"
    ],
  },
  {
    id: "rum_peach",
    name: "럼&피치",
    tagline: "상큼 달콤, 해변 산책!",
    color: "#f59e0b",
    ingredients: [
      { name: "럼", amount: 40, unit: "ml" },
      { name: "피치트리", amount: 20, unit: "ml" },
      { name: "오렌지주스", amount: 120, unit: "ml" },
      { name: "토닉", amount: 20, unit: "ml", note: "살짝" },
    ],
    howto: ["얼음 가득 잔에 빌드", "부드럽게 1–2회 스터"],
  },
  {
    id: "peach_crush",
    name: "피치크러시",
    tagline: "복숭아 x 크랜베리의 선셋!",
    color: "#ef4444",
    ingredients: [
      { name: "럼", amount: 30, unit: "ml" },
      { name: "피치트리", amount: 20, unit: "ml" },
      { name: "오렌지주스", amount: 80, unit: "ml" },
      { name: "크랜베리주스", amount: 40, unit: "ml" },
    ],
    howto: ["얼음 → 모든 재료 빌드", "색감 레이어를 살짝 유지"],
  },
  {
    id: "peach_highball",
    name: "피치트리 하이볼",
    tagline: "심플 이즈 베스트, 달달 하이볼",
    color: "#f97316",
    ingredients: [
      { name: "피치트리", amount: 45, unit: "ml" },
      { name: "토닉", amount: 120, unit: "ml" },
    ],
    howto: ["차가운 잔/얼음 → 피치트리 → 토닉", "1–2회만 스터"],
  },
  {
    id: "fiji_peach",
    name: "피지 피치트리",
    tagline: "피치 하이볼 + 라임의 상쾌함",
    color: "#22c55e",
    ingredients: [
      { name: "피치트리", amount: 45, unit: "ml" },
      { name: "토닉", amount: 120, unit: "ml" },
      { name: "라임", amount: 0.5, unit: "piece" },
    ],
    howto: ["피치트리와 토닉 빌드", "라임 웨지로 짜 넣고 가니시"],
  },
  {
    id: "peach_milk",
    name: "피치밀크",
    tagline: "달콤 크리미 디저트 잔",
    color: "#fb7185",
    ingredients: [
      { name: "피치트리", amount: 30, unit: "ml" },
      { name: "우유", amount: 90, unit: "ml" },
    ],
    howto: ["얼음 → 피치트리 → 우유", "가볍게 스터"],
  },
  {
    id: "jimbeam_highball",
    name: "짐빔 하이볼",
    tagline: "깔끔 시원, 모두의 하이볼",
    color: "#60a5fa",
    ingredients: [
      { name: "짐빔", amount: 45, unit: "ml" },
      { name: "토닉", amount: 150, unit: "ml" },
      { name: "레몬", amount: 0.15, unit: "piece", note: "가니시(1개로 6–8잔)" },
    ],
    howto: ["얼음 가득 → 위스키 → 차가운 토닉", "1–2회만 스터"],
  },
];

// 랜덤 미션 풀(공용 + 칵테일 전용 일부)
const COMMON_MISSIONS = [
  "왼손만 사용해서 젓기",
  "모두의 건배사 담당하기",
  "다음 잔 나올 때까지 영어만 쓰기",
  "다음 잔 나올 때까지 외래어 안쓰기",
  "10분간 금지어: '네'",
  "10분간 금지어: '형'",
  "10분간 금지어: '아니'",
  "10분간 금지어: '근데'",
  "10분간 금지어: '약간'",
  "10분간 금지어: '그러니까'",
  "10분간 금지어: '진짜'",
  "10분간 금지어: '뭔가'",
  "10분간 금지어: '솔직히'",
  "10분간 금지어: '맞아'",
  "10분간 금지어: '그리고'",
  "10분간 금지어: 'optimiztion'",
  "10분간 금지어: 'cocktail'",
  "사회자가 정해주는 단어 몸으로 말해요",
  "오늘 착장에 '흰색'이 포함된 사람에게 술 한잔 말아주기 (벌칙주 가능)",
  "모두에게 칭찬 한 마디씩 하기",
  "사회자에게 감사 인사하기",
  "집주인에게 감사 인사하기",
  "그룹장에게 감사 인사하기",
  "제일 피곤해보이는사람 술 말아주기 (벌칙주 가능)",
  "노래방에서 골든 완창 하기 (노래방 가서 하기)",
  "10초간 얼음만 바라보기 챌린지",
  "랜덤 게스트와 잔 바꿔 들고 포즈 찍기",
  "가장 시원한 표정 지어보기",
  "AI Data TF에서 가장 재수없는 사람은? (+팩폭 한마디)",
  "AI Data TF에서 가장 고마운 사람은? (+감사인사 한마디)",
  "우리 팀에서 자동화 하면 행복지수 오르는 작업 1개 (3인 이상 동의 시 성공)",
  "앉은 자리에서 오른쪽 옆사람과 러브샷",
  "칭찬 3연타: 오른쪽 사람의 장점 3가지 구체적으로 말하기", 
  "동료 중 디버깅 도움 1위에게 감사 한 마디", 
  "금지어 5개: AI, Data, Model, PPT, 장표 쓰지 않고 오늘 업무 설명",
  "리듬 박수: 사회자가 친 패턴 그대로 따라 치기 (3회 성공 시 성공)",
  "이구 동성: 사회자가 정해준 한명과 '하트' 동작 똑같이 하기",
  "이구 동성: 사회자가 정해준 한명과 '감사' 동작 똑같이 하기",
  "이구 동성: 사회자가 정해준 한명과 '노예' 동작 똑같이 하기",
  "눈싸움: 오른쪽 사람과 눈싸움 (이긴사람이 진 사람에게 벌칙주)", 
  "오른쪽 사람이 정한 숫자 맞추기 (0~99)",
  "귀엽고 깜찍한 포즈 (5인 이상 동의 시 성공)",
  "어부바: 오른쪽에 있는 사람 업고 3초 버티기",
  "오른쪽 사람이 정해주는 숫자의 팀 멤버에게 카톡으로 진지하게 감사 인사 하기 (이름 순)",
  "나보다 키 큰사람 다 마셔^^",
  "모두에게 인디언 밥~ 맞기",
  "오른쪽 사람이 만들어주는 안주 맛있게 먹기^^ (레몬 가능)",
  "나 빼고 다 원샷!", 
  "앉았다 일어났다 5회!", 
  "코끼리코 5바퀴!", 
  "오른쪽 사람이 정해주는 사진으로 하루동안 카톡 프사 하기 (킹받는 사진 가능)",
  "술자리 퀴즈왕 1개 뽑기", 
  "술자리 퀴즈왕 1개 뽑기", 
  "술자리 퀴즈왕 1개 뽑기", 
  "술자리 퀴즈왕 1개 뽑기", 
  "흑역사 썰 풀기 (3인 이상 동의 시 성공)",
  
];

const MISSION_BY_ID: Record<string, string[]> = {
  mojito: ["민트 잎으로 하트 모양 만들기", "라임 웨지로 미니 아트 만들기", "모히또 3행시"],
  rum_peach: ["복숭아 이모지만으로 감상 표현하기 🍑", "오른쪽 사람이 비율 조절"],
  peach_crush: ["선셋 사진 찍어 단톡방에 올리기"],
  peach_highball: ["하이볼 버블이 가장 많이 보이는 각도 찾기"],
  fiji_peach: ["라임 향을 맡고 한 줄 감상 쓰기"],
  peach_milk: ["한 모금 마시고 디저트 평론가처럼 묘사하기"],
  jimbeam_highball: ["가장 청량한 건배 멘트 만들기", "장원영 짐빔 하이볼 광고 따라하기^^", "오늘의 럭키비키 사고 하나"],
};

// -----------------------------
// 유틸
// -----------------------------
function formatAmount(i: Ingredient) {
  if (i.range) return `${i.range[0]}–${i.range[1]}ml`;
  if (i.unit === "ml") return `${i.amount}ml`;
  if (i.unit === "leaf") return `${i.amount}잎`;
  if (i.unit === "piece") return `${i.amount % 1 === 0 ? i.amount : i.amount.toString().replace("0.", ".")}개`;
  if (i.unit === "g") return `${i.amount}g`;
  return `${i.amount}`;
}

function randomFrom<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

// -----------------------------
// 메인 컴포넌트
// -----------------------------
export default function CocktailPartyMiniApp() {
  const [pickedId, setPickedId] = useState<string | null>(null);
  const picked = useMemo(() => RECIPES.find(r => r.id === pickedId) || null, [pickedId]);
  const [mission, setMission] = useState<string>("");

  const reroll = (id?: string) => {
    const key = id || pickedId || RECIPES[0].id;
    const pool = [...COMMON_MISSIONS, ...(MISSION_BY_ID[key] || [])];
    setMission(randomFrom(pool));
  };

  React.useEffect(() => {
    if (!pickedId && RECIPES.length) setPickedId(RECIPES[0].id);
  }, []);

  React.useEffect(() => {
    if (pickedId) reroll(pickedId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pickedId]);

  const copyRecipe = async () => {
    const text = picked
      ? `${picked.name} — ${picked.tagline}\n\n재료:\n` +
        picked.ingredients
          .map((i) => `• ${i.name}: ${formatAmount(i)}${i.note ? ` (${i.note})` : ""}`)
          .join("\n") +
        (picked.howto?.length ? `\n\n만드는 법:\n` + picked.howto.map((s) => `• ${s}`).join("\n") : "") +
        (mission ? `\n\n오늘의 랜덤 미션: ${mission}` : "")
      : "";
    try {
      await (navigator as any).clipboard.writeText(text);
      alert("레시피를 클립보드에 복사했어요!");
    } catch {
      alert("복사에 실패했습니다. 수동으로 선택해 복사해 주세요.");
    }
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-neutral-50 to-neutral-100 text-neutral-900 p-4 md:p-8">
      <div className="mx-auto max-w-6xl">
        <header className="flex items-center gap-3 mb-6">
          <Martini className="w-7 h-7" />
          <h1 className="text-2xl md:text-3xl font-bold">칵테일 파티 – 랜덤 미션 & 레시피</h1>
          <Badge className="ml-auto">MVP</Badge>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* 좌측: 칵테일 선택 */}
          <div className="md:col-span-1 space-y-3">
            {RECIPES.map((r) => (
              <Card
                key={r.id}
                className={`cursor-pointer transition hover:shadow-md ${pickedId === r.id ? "ring-2 ring-offset-2" : ""}`}
                onClick={() => setPickedId(r.id)}
                style={{ borderColor: pickedId === r.id ? r.color : undefined }}
              >
                <CardContent className="p-4 flex items-center justify-between">
                  <div>
                    <div className="font-semibold">{r.name}</div>
                    <div className="text-sm text-neutral-500">{r.tagline}</div>
                  </div>
                  <div className="w-6 h-6 rounded-full" style={{ backgroundColor: r.color }} />
                </CardContent>
              </Card>
            ))}
          </div>

          {/* 우측: 상세 */}
          <div className="md:col-span-2">
            {picked && (
              <motion.div
                key={picked.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
              >
                <Card className="overflow-hidden">
                  <div className="h-2" style={{ backgroundColor: picked.color }} />
                  <CardContent className="p-6">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="w-5 h-5" />
                      <h2 className="text-xl font-bold">{picked.name}</h2>
                      <Badge variant="secondary" className="ml-2">{picked.tagline}</Badge>
                    </div>

                    <section className="mt-4">
                      <h3 className="font-semibold mb-2">오늘의 랜덤 미션</h3>
                      <div className="flex items-center gap-3">
                        <div className="text-lg">{mission}</div>
                        <Button size="sm" variant="outline" onClick={() => reroll()} className="gap-2">
                          <RefreshCw className="w-4 h-4" /> 다시 뽑기
                        </Button>
                      </div>
                    </section>

                    <section className="mt-6">
                      <h3 className="font-semibold mb-2">레시피</h3>
                      <ul className="space-y-1">
                        {picked.ingredients.map((i, idx) => (
                          <li key={idx} className="text-[15px]">
                            <span className="font-medium">{i.name}</span>: {formatAmount(i)}
                            {i.note ? <span className="text-neutral-500"> ({i.note})</span> : null}
                          </li>
                        ))}
                      </ul>
                      {picked.howto && (
                        <div className="mt-3 text-sm text-neutral-700">
                          <div className="font-medium mb-1">만드는 법</div>
                          <ol className="list-decimal pl-5 space-y-1">
                            {picked.howto.map((s, i) => <li key={i}>{s}</li>)}
                          </ol>
                        </div>
                      )}
                      <div className="mt-4 flex gap-2">
                        <Button onClick={copyRecipe} className="gap-2">
                          <Copy className="w-4 h-4" /> 레시피 복사
                        </Button>
                      </div>
                    </section>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </div>
        </div>

        <footer className="mt-8 text-center text-xs text-neutral-500">
          © {new Date().getFullYear()} Cocktail Party Helper — have fun & drink responsibly 🍸
        </footer>
      </div>
    </div>
  );
}
