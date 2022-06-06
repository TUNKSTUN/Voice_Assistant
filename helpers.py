import random


query_helper = """
MDTextField:
    hint_text: "How can I help you?"
    helper_text: "what's the weather today?"
    helper_text_mode: "on_focus"
    icon_right: "android"
    icon_right_color: self.theme_cls.primary_color
    pos_hint: {"center_x": 0.5, "center_y": 0.7}
    size_hint_x: None
    width: 300
"""

toolbar_helper = """
Screen:
    BoxLayout:
        orientation:'vertical'
        MDToolbar:
            title:'Assistant'
            elevation:10
            md_bg_color: app.theme_cls.primary_color

        Widget:

        MDBottomAppBar:
            MDToolbar:
                type: 'bottom'
                on_action_button: app.questions_1_1_img()
"""


# year - I sem - I

questions_img_I_I = """
ScreenManager:
    I_I_subjects_img:
    I_I_mathematics_questions_img:


<I_I_subjects_img>:
    name: "subjects_I_I_img"
    MDRectangleFlatButton:
        text: "Mathematics - I"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.8}
        on_press: root.manager.current = "mathematics_img"
        
    MDRectangleFlatButton:
        text: "Chemistry"
        font_size: "30sp"
        pos_hint: {"x": 0.4, "y": 0.6}
        
    MDRectangleFlatButton:
        text: "Basic Electrical Engineering"
        font_size: "30sp"
        pos_hint: {"x": 0.25, "y": 0.4}
        
    MDRectangleFlatButton:
        text: "English"
        font_size: "30sp"
        pos_hint: {"x": 0.42, "y": 0.2}
    
    
<I_I_mathematics_questions_img>:
    name: "mathematics_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(5), dp(5)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "mai-san.jpg"
                text: "[size=26]mai-san[/size]"
                
            SmartTileWithLabel:
                source: "franxx.jpg"
                text: "[size=26]franxx[/size]"
                
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "subjects_I_I_img"

"""


# year - I sem - II (pending!...)

# year - II sem - I (pending!...)

# year - II sem - II (pending!...)

# year - III sem - I (pending!...)

# year - III sem - II (pending!...)


