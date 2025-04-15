// pages/api/chat.js
import { OpenAI } from "openai";
const openai = new OpenAI({ apiKey: process.env.AZURE_OPENAI_API_KEY });

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  const { messages } = req.body;
  const completion = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [...messages],
    temperature: 0.7,
  });

  const reply = completion.choices[0].message.content;

  let insights = null;
  try {
    const match = reply.match(/\{[\s\S]*\}/);
    if (match) insights = JSON.parse(match[0]);
  } catch {}

  res.status(200).json({ reply, insights });
}
