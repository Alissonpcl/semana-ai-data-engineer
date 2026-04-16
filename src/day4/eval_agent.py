"""ShopAgent Day 4 — DeepEval evaluation for tool routing and answer quality."""

import sys
from pathlib import Path

from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

TEST_MATRIX = [
    {
        "input": "Qual o faturamento total por estado?",
        "actual_output": "SP: R$ 127.430, RJ: R$ 89.210, MG: R$ 68.440",
        "tools_called": [ToolCall(name="supabase_execute_sql")],
        "expected_tools": [ToolCall(name="supabase_execute_sql")],
    },
    {
        "input": "Quantos pedidos foram feitos por pix?",
        "actual_output": "1.847 pedidos pagos via pix (45% do total).",
        "tools_called": [ToolCall(name="supabase_execute_sql")],
        "expected_tools": [ToolCall(name="supabase_execute_sql")],
    },
    {
        "input": "Qual o ticket medio por segmento de cliente?",
        "actual_output": "Premium: R$ 487, Standard: R$ 234, Basic: R$ 112",
        "tools_called": [ToolCall(name="supabase_execute_sql")],
        "expected_tools": [ToolCall(name="supabase_execute_sql")],
    },
    {
        "input": "Quais clientes reclamam de entrega?",
        "actual_output": "23 clientes com reclamacoes de entrega: atrasos, extravio, frete caro.",
        "retrieval_context": [
            "Demorou 15 dias para chegar.",
            "Nao recebi meu pedido ate hoje.",
            "Frete caro demais para a regiao Norte.",
        ],
        "tools_called": [ToolCall(name="qdrant_semantic_search")],
        "expected_tools": [ToolCall(name="qdrant_semantic_search")],
    },
    {
        "input": "O que os clientes falam sobre qualidade dos produtos?",
        "actual_output": "Maioria positiva. 12% citam problemas com durabilidade.",
        "retrieval_context": [
            "Produto otimo, superou expectativas!",
            "Qualidade boa pelo preco.",
            "Quebrou em 2 semanas de uso.",
        ],
        "tools_called": [ToolCall(name="qdrant_semantic_search")],
        "expected_tools": [ToolCall(name="qdrant_semantic_search")],
    },
    {
        "input": "Qual o sentimento geral sobre o frete?",
        "actual_output": "67% negativo. Principais queixas: prazo e custo.",
        "retrieval_context": [
            "Frete caro demais.",
            "Chegou antes do previsto, otimo!",
            "Rastreamento nao funciona direito.",
        ],
        "tools_called": [ToolCall(name="qdrant_semantic_search")],
        "expected_tools": [ToolCall(name="qdrant_semantic_search")],
    },
]


def build_test_cases() -> list[LLMTestCase]:
    return [LLMTestCase(**case) for case in TEST_MATRIX]


def run_tool_correctness(test_cases: list[LLMTestCase]) -> list[dict]:
    metric = ToolCorrectnessMetric(threshold=1.0)
    results = []
    for tc in test_cases:
        metric.measure(tc)
        results.append({
            "input": tc.input,
            "score": metric.score,
            "passed": metric.score >= metric.threshold,
            "expected": tc.expected_tools[0].name if tc.expected_tools else None,
            "actual": tc.tools_called[0].name if tc.tools_called else None,
        })
    return results


def run_answer_relevancy(test_cases: list[LLMTestCase]) -> list[dict]:
    metric = AnswerRelevancyMetric(
        threshold=0.7,
        model="claude-sonnet-4-20250514",
        include_reason=True,
    )
    results = []
    for tc in test_cases:
        metric.measure(tc)
        results.append({
            "input": tc.input,
            "score": metric.score,
            "passed": metric.score >= metric.threshold,
            "reason": metric.reason,
        })
    return results


def run_full_evaluation() -> None:
    test_cases = build_test_cases()

    print("=" * 60)
    print("  ShopAgent Evaluation -- Tool Correctness")
    print("=" * 60)

    tool_results = run_tool_correctness(test_cases)
    passed = sum(1 for r in tool_results if r["passed"])
    total = len(tool_results)

    for r in tool_results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['input'][:50]}")
        print(f"         expected={r['expected']}, actual={r['actual']}, score={r['score']}")

    print(f"\n  Tool Correctness: {passed}/{total} passed")

    print()
    print("=" * 60)
    print("  ShopAgent Evaluation -- Answer Relevancy")
    print("=" * 60)

    relevancy_results = run_answer_relevancy(test_cases)
    passed_rel = sum(1 for r in relevancy_results if r["passed"])

    for r in relevancy_results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['input'][:50]}")
        print(f"         score={r['score']:.2f} | {r['reason'][:80] if r['reason'] else ''}")

    print(f"\n  Answer Relevancy: {passed_rel}/{total} passed")

    print()
    print("=" * 60)
    print("  Batch Evaluation (deepeval.evaluate)")
    print("=" * 60)

    tool_metric = ToolCorrectnessMetric(threshold=1.0)
    relevancy_metric = AnswerRelevancyMetric(
        threshold=0.7,
        model="claude-sonnet-4-20250514",
        include_reason=True,
    )

    batch_results = evaluate(
        test_cases=test_cases,
        metrics=[tool_metric, relevancy_metric],
    )

    print(f"\n  Batch evaluation complete: {len(test_cases)} test cases")

    all_passed = all(r["passed"] for r in tool_results) and all(
        r["passed"] for r in relevancy_results
    )
    if not all_passed:
        print("\n  WARNING: Some evaluations failed. Review results above.")
        sys.exit(1)


if __name__ == "__main__":
    run_full_evaluation()
