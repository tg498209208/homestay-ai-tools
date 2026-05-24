---
name: agent-kpi-analysis
description: BMW Financial Services AI Agent KPI analysis methodology. Use when optimizing AI analysis prompts, reviewing generated insights quality, or iterating on the monthly report AI output.
---

# Agent KPI Analysis Skill

## When to Use

- Optimizing the AI-generated insights in Agent Monthly Report (`ai-insights-service.ts`)
- Reviewing and improving the quality of generated analysis bullet points
- Iterating on system/user prompts for Azure OpenAI
- Adding new KPI metrics or adjusting analysis logic

## Business Context

BMW Financial Services China operates 4 AI Agents across two business lines:
- **AFC CC** / **HIL CC**: Contact Center agents (full-service, including voice)
- **AFC OCC** / **HIL OCC**: Online Customer Center agents (text-only)

The monthly report is presented to the **client's execution team**, who will forward key insights to **senior management**. Therefore the tone must be professional, management-friendly, and constructively positive.

## KPI Definitions & Targets

| KPI | Formula | Target | Notes |
|-----|---------|--------|-------|
| **综合转人工率** | (wechatHuman + ivrSmartHuman) / (wechatTotal + callsTotal) | -- | For reference only, not a KPI target |
| **文本渠道转人工率** | wechatHuman / wechatTotal | < 15% | **Core KPI** - text channel is fully controlled by us |
| **IVR 转人工率** | ivrSmartHuman / ivrSmartTotal | -- | Not assessed (controlled by another team) |
| **FCR** | First Contact Resolution | > 80% | Stored as decimal in DB (0.85 = 85%) |
| **CSS** | Customer Satisfaction Score | > 4.25 | Scale 0-5, CC agents only |
| **NPS** | Net Promoter Score | > 70 | Scale 0-100, CC agents only |
| **语音使用率** | wechatVoice / wechatTotal | -- | No target; used to evaluate voice feature ROI |

### KPI Priority for Analysis
1. **P0 (Must mention if anomalous)**: 文本渠道转人工率, FCR
2. **P1 (Mention for CC agents)**: CSS, NPS
3. **P2 (Context/background)**: 综合转人工率, 会话量变化, 语音使用率
4. **Not assessed**: IVR 转人工率 (mention only as context, never as a concern)

## Analysis Framework

### Data to Provide AI
- Full historical data (all available months, typically 2-3 years)
- Current month + previous month for MoM calculation
- Same month last year for YoY calculation
- KPI targets for benchmark comparison

### Output Structure (5 bullet points)
```
1. [核心表现] 本月整体表现概述，对标KPI目标值
2. [环比变化] 环比显著变化的指标（阈值: ±10% 或 ±2百分点）
3. [同比趋势] 同比变化或长期趋势观察
4. [亮点/风险] 具体亮点或需关注的风险点
5. [建议方向] 可操作的运营建议
```

### Tone & Style Rules
- Language: Chinese with English acronyms (FCR, NPS, CSS, IVR)
- Perspective: Management-friendly, professional
- Sentiment: Constructively positive — highlight achievements first, then areas for improvement
- Phrasing: Use "数据显示", "表现优异", "建议持续关注", "环比提升/下降"
- Avoid: "可能是因为", "应该是", subjective speculation
- For targets: Say "达标" / "超额达标" when meeting target; "接近目标" or "建议重点关注" when below

### Special Business Rules
- **Text transfer rate is the core KPI** — IVR transfer rate is not assessed
- **Voice usage rate** is for ROI tracking only, not a performance indicator
- **OCC agents** don't have NPS/CSS — skip those metrics
- When a metric has no data ("--"), state it factually without speculation
- **Portfolio size** (CC only) is manual data; if missing, note it neutrally

## Prompt Engineering Guidelines

### System Prompt Best Practices
- Define the role clearly: "BMW 金融服务中国 AI Agent 运营高级分析师"
- Include KPI targets in the system prompt so AI can benchmark
- Specify the output structure explicitly
- Set temperature to 0.3 for consistent, analytical output
- Use few-shot examples when available

### User Prompt Best Practices
- Provide data in structured table format for clarity
- Include YoY data (same month last year) alongside MoM
- Pre-calculate all rates and deltas — don't ask AI to compute
- Mark which metrics are above/below target

## Validation Checklist

When reviewing AI-generated insights:
- [ ] All 5 bullet points follow the specified structure
- [ ] Core KPIs (transfer rate, FCR) are mentioned
- [ ] KPI targets are referenced (达标/未达标)
- [ ] Both MoM and YoY changes are covered
- [ ] Tone is professional and constructively positive
- [ ] No subjective speculation ("可能是因为...")
- [ ] IVR transfer rate is NOT flagged as a concern
- [ ] OCC agents don't mention NPS/CSS
- [ ] Each bullet is under 100 characters
- [ ] Chinese text with English acronyms only

## File References

- AI Service: `src/plugins/agent-monthly-report/services/ai-insights-service.ts`
- Calculation Utils: `src/plugins/agent-monthly-report/utils/calculation-utils.ts`
- Constants: `src/plugins/agent-monthly-report/constants.ts`
- Types: `src/plugins/agent-monthly-report/types.ts`
- Display: `src/plugins/agent-monthly-report/components/AgentInsightsPage.tsx`
