import gradio as gr
from DataModule.AzureBlobStorage import AzureBlobStorage
from AnalyticModule.DocumentAnalysis import DocumentAnalysis
from AnalyticModule.TextAnalysis import TextAnalytics
from AnalyticModule.AzureOpenAIChat import AzureOpenAIChat
from APIModule.KopisAPI import KopisAPI
from ChartModule.BasicChart import BasicChart

# d3.js로 인터페이스 변경 
# def create_gradio_interface():
#     # 객체 생성
#     blob_storage = AzureBlobStorage()
#     doc_analysis = DocumentAnalysis()
#     text_analytics = TextAnalytics()
#     chatbot = AzureOpenAIChat()
#     kopis_api = KopisAPI()
#     basic_chart = BasicChart()

#     def update_performance_table():
#         headers, data = kopis_api.fetch_performance_list()
#         return gr.update(headers=headers, value=data)
#     # 통계 유형에 따른 태그만 미리 불러오기
#     def fetch_headers(mode):
#         headers, _ = kopis_api.fetch_statistics_data(mode=mode)
#         return gr.update(choices=headers, value=headers[0]), gr.update(choices=headers, value=headers[1])
    
#     with gr.Blocks(css=".gradio-container {padding: 2rem;}") as demo:
#         gr.Markdown(
#             """
#             # 🎭 Performing Arts Insight
#             **공연 예술 데이터를 분석하고 시각화하는 통합 플랫폼**  
#             ---
#             """,
#         )
#         with gr.Row():  # Row로 두 부분을 나눔
#             with gr.Column(scale=3):  # 챗봇 영역: 4/10
#                 chatbot_output = gr.Chatbot(label="Bot Response", type='messages')  # 챗봇 대화 창
#                 chatbot_input = gr.Textbox(label="Chat with the bot", placeholder="Type your message here...", show_label=False)
#                 chatbot_input.submit(chatbot.chatgpt_response, inputs=[chatbot_input, chatbot_output], outputs=[chatbot_output, chatbot_output])

#             with gr.Column(scale=7):  # 탭 영역: 6/10
#                 with gr.Tab("Business Report Analysis"):
#                     file_input = gr.File(label="Upload Document")
#                     output_text = gr.Textbox(label="Extracted Text")
#                     file_input.change(doc_analysis.analyze_document, inputs=file_input, outputs=output_text)
                
#                 with gr.Tab("Audience Review Analysis"):
#                     review_input = gr.Textbox(lines=5, label="Audience Review Input(줄바꿈으로 여러 문장 가능)")
#                     analysis_button = gr.Button("Let's Analyze!")
#                     analysis_output = gr.JSON(label="Analysis Results")
#                     analysis_button.click(fn=text_analytics.analze_review, inputs=review_input, outputs=analysis_output)

#                 with gr.Tab("OpenAPI Data - 공연 목록(표)"):
#                     fetch_button = gr.Button("Fetch Performance List")
#                     openapi_output = gr.Dataframe()
#                     poster_images = gr.Gallery(label="Posters", show_label=False, columns=[2], height=400)
#                     fetch_button.click(fn=update_performance_table, outputs=openapi_output)
#                     fetch_button.click(fn=kopis_api.fetch_posters_only, outputs=poster_images)

#                 with gr.Tab("OpenAPI Data - 기간별 통계(그래프)"):
#                     mode_dropdown = gr.Dropdown(label="통계 유형 선택", choices=["period", "genre"], value="period")
#                     fetch_btn = gr.Button("📊 항목 불러오기")

#                     x_axis = gr.Dropdown(label="X축 항목", choices=[])
#                     y_axis = gr.Dropdown(label="Y축 항목", choices=[])

#                     draw_btn = gr.Button("📈 그래프 그리기")
#                     plot_output = gr.Plot(label="통계 시각화 결과")

#                     # 통계 유형을 선택하고 fetch할 때 헤더 선택지 업데이트
#                     fetch_btn.click(fetch_headers, inputs=mode_dropdown, outputs=[x_axis, y_axis])
#                     draw_btn.click(
#                         fn=lambda mode, x, y: basic_chart.show_statistics_chart(mode, x_index=x, y_index=y),
#                         inputs=[mode_dropdown, x_axis, y_axis],
#                         outputs=plot_output
#                     )
#     return demo

# # 실행
# if __name__ == "__main__":
#     gr_interface = create_gradio_interface()
#     gr_interface.launch(share=True)  # 'share=True'로 공유 링크를 생성
