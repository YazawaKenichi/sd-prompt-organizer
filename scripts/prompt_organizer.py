import modules.scripts as scripts
import gradio as gr

from modules.processing import StableDiffusionProcessing

class ExtensionTemplateScript(scripts.Script):
    def title(self):
        return "Prompt Organizer"
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    def ui(self, is_img2img):
        with gr.Accordion(self.title(), open = False):
            with gr.Row():
                enabled = gr.Checkbox(False, label="Enable")
            with gr.Row():
                with gr.Column(scale = 1):
                    prePositiveEnabled = gr.Checkbox(False, label="Enable Positive Prefix")
                    prePositive = gr.Textbox(
                        info="Inserted before the main prompt",
                        label= "Positive Prefix",
                        lines=3,
                        value=""
                        )
                with gr.Column(scale = 1):
                    postPositiveEnabled = gr.Checkbox(False, label="Enable Positive Postfix")
                    postPositive = gr.Textbox(
                        info="Inserted after the main prompt",
                        label= "Positive Postfix",
                        lines=3,
                        value=""
                        )
            with gr.Row():
                with gr.Column(scale = 1):
                    preNegativeEnabled = gr.Checkbox(False, label="Enable Negative Prefix")
                    preNegative = gr.Textbox(
                        info="Inserted before the main negative prompt",
                        label= "Negative Prefix",
                        lines=3,
                        value=""
                        )
                with gr.Column(scale = 1):
                    postNegativeEnabled = gr.Checkbox(False, label="Enable Negative Postfix")
                    postNegative = gr.Textbox(
                        info="Inserted after the negative prompt",
                        label= "Negative Postfix",
                        lines=3,
                        value=""
                        )
        return [enabled, prePositiveEnabled, postPositiveEnabled, preNegativeEnabled, postNegativeEnabled, prePositive, postPositive, preNegative, postNegative]

    def process(self, p: StableDiffusionProcessing, enabled, prePositiveEnabled, postPositiveEnabled, preNegativeEnabled, postNegativeEnabled, prePositive, postPositive, preNegative, postNegative):
        if not enabled:
           return
        prompt = p.prompt
        negative_prompt = p.negative_prompt
        if prePositive and prePositiveEnabled:
           prompt = prePositive + ", " + prompt
        if postPositive and postPositiveEnabled:
           prompt = prompt + ", " + postPositive
        if preNegative and preNegativeEnabled:
           negative_prompt = preNegative + ", " + negative_prompt
        if postNegative and postNegativeEnabled:
           negative_prompt = negative_prompt + ", " + postNegative
        p.all_prompts[0] = prompt
        p.all_negative_prompts[0] = negative_prompt
