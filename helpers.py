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
                on_action_button: app.execute_assistant()
"""


# year - I sem - I

questions_img_I_I = """
ScreenManager:
    I_I_subjects_img:
    I_I_mathematics_prev_img:
    I_I_chemistry_prev_img:
    I_I_electrical_engineering_prev_img:
    I_I_english_prev_img:


<I_I_subjects_img>:
    name: "I_I_subjects_img"
    MDRectangleFlatButton:
        text: "Mathematics - I"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.8}
        on_press: root.manager.current = "mathematics_img"
        
    MDRectangleFlatButton:
        text: "Chemistry"
        font_size: "30sp"
        pos_hint: {"x": 0.4, "y": 0.6}
        on_press: root.manager.current = "chemistry_img"
        
    MDRectangleFlatButton:
        text: "Basic Electrical Engineering"
        font_size: "30sp"
        pos_hint: {"x": 0.25, "y": 0.4}
        on_press: root.manager.current = "electrical_engineering_img"
        
    MDRectangleFlatButton:
        text: "English"
        font_size: "30sp"
        pos_hint: {"x": 0.42, "y": 0.2}
        on_press: root.manager.current = "english_img"
        
    MDRectangleFlatButton:
        text: "Main Screen"
        font_size: '30sp'
        pos_hint: {"x": 0.17, "y": 0.2}
        on_press: app.restart()

    
<I_I_mathematics_prev_img>:
    name: "mathematics_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "mathematics_1_r16_01.jpg"
                text: "[size=26]Mathematics (R16)[/size]"
                
            SmartTileWithLabel:
                source: "mathematics_1_r16_02.jpg"
                text: "[size=26]Mathematics (R16)[/size]"
                
            SmartTileWithLabel:
                source: "mathematics_1_r18_01.jpg"
                text: "[size=26]Mathematics (R18)[/size]"
                
            SmartTileWithLabel:
                source: "mathematics_1_r18_02.jpg"
                text: "[size=26]Mathematics (R18)[/size]"
                
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "I_I_subjects_img"
                
<I_I_chemistry_prev_img>:
    name: "chemistry_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "chemistry_r16_01.jpg"
                text: "[size=26]Chemistry (R16)[/size]"
                
            SmartTileWithLabel:
                source: "chemistry_r16_02.jpg"
                text: "[size=26]Chemistry (R16)[/size]"
                
            SmartTileWithLabel:
                source: "chemistry_r18_01.jpg"
                text: "[size=26]Chemistry (R18)[/size]"
                
            SmartTileWithLabel:
                source: "chemistry_r18_02.jpg"
                text: "[size=26]Chemistry (R18)[/size]"
                
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "I_I_subjects_img"
                
<I_I_electrical_engineering_prev_img>
    name: "electrical_engineering_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "BEE_r16_01.jpg"
                text: "[size=26]Basic Electrical And Electronic Engineering (R16)[/size]"
                
            SmartTileWithLabel:
                source: "BEE_r16_02.jpg"
                text: "[size=26]Basic Electrical And Electronic Engineering (R16)[/size]"
                
            SmartTileWithLabel:
                source: "BEE_r18_01.jpg"
                text: "[size=26]Basic Electrical Engineering (R18)[/size]"
                
            SmartTileWithLabel:
                source: "BEE_r18_02.jpg"
                text: "[size=26]Basic Electrical Engineering (R18)[/size]"
                
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "I_I_subjects_img"
                
<I_I_english_prev_img>
    name: "english_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "english_r16_01.jpg"
                text: "[size=26]English (R16)[/size]"
                
            SmartTileWithLabel:
                source: "english_r16_02.jpg"
                text: "[size=26]English (R16)[/size]"
                
            SmartTileWithLabel:
                source: "english_r16_03.jpg"
                text: "[size=26]English (R16)[/size]"
                
            SmartTileWithLabel:
                source: "english_r18_01.jpg"
                text: "[size=26]English (R18)[/size]"
                
            SmartTileWithLabel:
                source: "english_r18_02.jpg"
                text: "[size=26]English (R18)[/size]"
                
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "I_I_subjects_img"
    

"""

# year - I sem - II

questions_img_I_II = """
ScreenManager:
    I_II_subjects_img:
    I_II_mathematics_II_prev_img:
    I_II_applied_physics_prev_img:
    I_II_PPS_prev_img:


<I_II_subjects_img>:
    name: "I_II_subjects_img"
    MDRectangleFlatButton:
        text: "Mathematics - II"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.8}
        on_press: root.manager.current = "mathematics_II_img"

    MDRectangleFlatButton:
        text: "Applied Physics"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.6}
        on_press: root.manager.current = "applied_physics_img"

    MDRectangleFlatButton:
        text: "Programming For Problem Solving"
        font_size: '30sp'
        pos_hint: {"x": 0.24, "y": 0.4}
        on_press: root.manager.current = "pps_img"
        
    MDRectangleFlatButton:
        text: "Main Screen"
        font_size: '30sp'
        pos_hint: {"x": 0.37, "y": 0.2}
        on_press: app.restart()

        
<I_II_mathematics_II_prev_img>:
    name: "mathematics_II_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "mathematics_2_r16_01.jpg"
                text: "[size=26]mathematics - 2 (R16)[/size]"
                
            SmartTileWithLabel:
                source: "mathematics_2_r16_02.jpg"
                text: "[size=26]mathematics - 2 (R16)[/size]"
                
            SmartTileWithLabel:
                source: "mathematics_2_r18_01.jpg"
                text: "[size=26]mathematics - 2 (R18)[/size]"
                
            SmartTileWithLabel:
                source: "mathematics_2_r18_02.jpg"
                text: "[size=26]mathematics - 2 (R18)[/size]"
                
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "I_II_subjects_img"
                
<I_II_applied_physics_prev_img>:
    name: "applied_physics_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "physics_r16_01.jpg"
                text: "[size=26]Engineering Physics (R16)[/size]"
                
            SmartTileWithLabel:
                source: "physics_r16_02.jpg"
                text: "[size=26]Engineering Physics (R16)[/size]"
                
            SmartTileWithLabel:
                source: "physics_r18_01.jpg"
                text: "[size=26]Applied Physics (R18)[/size]"
                
            SmartTileWithLabel:
                source: "physics_r18_02.jpg"
                text: "[size=26]Applied Physics (R18)[/size]"
                
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "I_II_subjects_img"

<I_II_PPS_prev_img>:
    name: "pps_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "c_r16_01.jpg"
                text: "[size=26]Computer Programming In C (R16)[/size]"
                    
            SmartTileWithLabel:
                source: "c_r16_02.jpg"
                text: "[size=26]Computer Programming In C (R16)[/size]"
    
            SmartTileWithLabel:
                source: "pps_r18_01.jpg"
                text: "[size=26]Programming For Problem Solving (R18)[/size]"
                    
            SmartTileWithLabel:
                source: "pps_r18_02.jpg"
                text: "[size=26]Programming For Problem Solving (R18)[/size]"
    
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "I_II_subjects_img"

"""

# year - II sem - I

questions_img_II_I = """
ScreenManager:
    II_I_subjects_img:
    II_I_ADE_prev_img:
    II_I_COA_prev_img:
    II_I_COSM_prev_img:
    II_I_data_structures_prev_img:
    II_I_OOP_prev_img:
    
<II_I_subjects_img>:
    name: "II_I_subjects_img"
    MDRectangleFlatButton:
        text: "Analog And Digital Electronics"
        font_size: '30sp'
        pos_hint: {"x": 0.26, "y": 0.9}
        on_press: root.manager.current = "ade_img"

    MDRectangleFlatButton:
        text: "Computer Organization And Architecture"
        font_size: '30sp'
        pos_hint: {"x": 0.17, "y": 0.7}
        on_press: root.manager.current = "coa_img"

    MDRectangleFlatButton:
        text: "Computer Oriented Statistical Methods"
        font_size: '30sp'
        pos_hint: {"x": 0.18, "y": 0.5}
        on_press: root.manager.current = "cosm_img"
    
    MDRectangleFlatButton:
        text: "Data Structures"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.3}
        on_press: root.manager.current = "data_structures_img"
        
    MDRectangleFlatButton:
        text: "Object Oriented Programming Using C++"
        font_size: '30sp'
        pos_hint: {"x": 0.16, "y": 0.1}
        on_press: root.manager.current = "oop_img"
        
    MDRectangleFlatButton:
        text: "Main Screen"
        font_size: '30sp'
        pos_hint: {"x": 0.1, "y": 0.3}
        on_press: app.restart()

        
<II_I_ADE_prev_img>:
    name: "ade_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "ade_r16_01.jpg"
                text: "[size=26]Digital Logic Design (R16)[/size]"
                    
            SmartTileWithLabel:
                source: "ade_r16_02.jpg"
                text: "[size=26]Digital Logic Design (R16)[/size]"
                
            SmartTileWithLabel:
                source: "ade_r18_01.jpg"
                text: "[size=26]Analog And Digital Electronics (R18)[/size]"
                
            SmartTileWithLabel:
                source: "ade_r18_02.jpg"
                text: "[size=26]Analog And Digital Electronics (R18)[/size]"

                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_I_subjects_img"

<II_I_COA_prev_img>:
    name: "coa_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "coa_r16_01.jpg"
                text: "[size=26]Computer Organization And Architecture (R16)[/size]"
                
            SmartTileWithLabel:
                source: "coa_r16_02.jpg"
                text: "[size=26]Computer Organization And Architecture (R16)[/size]"
                
            SmartTileWithLabel:
                source: "coa_r18_01.jpg"
                text: "[size=26]Computer Organization And Architecture (R18)[/size]"
                    
            SmartTileWithLabel:
                source: "coa_r18_02.jpg"
                text: "[size=26]Computer Organization And Architecture (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_I_subjects_img"

<II_I_COSM_prev_img>:
    name: "cosm_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "cosm_r16_01.jpg"
                text: "[size=26]Computer Oriented Statistical Method (R16)[/size]"
                
            SmartTileWithLabel:
                source: "cosm_r16_02.jpg"
                text: "[size=26]Computer Oriented Statistical Method (R16)[/size]"
                
            SmartTileWithLabel:
                source: "cosm_r18_01.jpg"
                text: "[size=26]Computer Oriented Statistical Method (R18)[/size]"
                    
            SmartTileWithLabel:
                source: "cosm_r18_02.jpg"
                text: "[size=26]Computer Oriented Statistical Method (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_I_subjects_img"
            
<II_I_data_structures_prev_img>:
    name: "data_structures_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "ds_r16_01.jpg"
                text: "[size=26]Data Structures (R16)[/size]"
                
            SmartTileWithLabel:
                source: "ds_r16_02.jpg"
                text: "[size=26]Data Structures (R16)[/size]"
                
            SmartTileWithLabel:
                source: "ds_r18_01.jpg"
                text: "[size=26]Data Structures (R18)[/size]"
                
            SmartTileWithLabel:
                source: "ds_r18_02.jpg"
                text: "[size=26]Data Structures (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_I_subjects_img"
            
<II_I_OOP_prev_img>:
    name: "oop_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "oop_r16_01.jpg"
                text: "[size=26]Object Oriented Programming Using Java (R16)[/size]"
                    
            SmartTileWithLabel:
                source: "oop_r16_02.jpg"
                text: "[size=26]Object Oriented Programming Using Java (R16)[/size]"
                
            SmartTileWithLabel:
                source: "oop_r18_01.jpg"
                text: "[size=26]Object Oriented Programming Using Java (R18)[/size]"
                
            SmartTileWithLabel:
                source: "oop_r18_02.jpg"
                text: "[size=26]Object Oriented Programming Using Java (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_I_subjects_img"
    
"""

# year - II sem - II

questions_img_II_II = """
ScreenManager:
    II_II_subjects_img:
    II_II_BEFA_prev_img:
    II_II_DBMS_prev_img:
    II_II_discrete_mathematics_prev_img:
    II_II_java_programming_prev_img:
    II_II_operating_system_prev_img:
    
<II_II_subjects_img>:
    name: "II_II_subjects_img"
    MDRectangleFlatButton:
        text: "Business Economics And Financial Analysis"
        font_size: '30sp'
        pos_hint: {"x": 0.17, "y": 0.9}
        on_press: root.manager.current = "befa_img"

    MDRectangleFlatButton:
        text: "Database Management System"
        font_size: '30sp'
        pos_hint: {"x": 0.25, "y": 0.7}
        on_press: root.manager.current = "dbms_img"

    MDRectangleFlatButton:
        text: "Discrete Mathematics"
        font_size: '30sp'
        pos_hint: {"x": 0.31, "y": 0.5}
        on_press: root.manager.current = "discrete_mathematics_img"
    
    MDRectangleFlatButton:
        text: "Java Programming"
        font_size: '30sp'
        pos_hint: {"x": 0.34, "y": 0.3}
        on_press: root.manager.current = "java_img"
        
    MDRectangleFlatButton:
        text: "Operating System"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.1}
        on_press: root.manager.current = "operating_system_img"
        
    MDRectangleFlatButton:
        text: "Main Screen"
        font_size: '30sp'
        pos_hint: {"x": 0.12, "y": 0.1}
        on_press: app.restart()

        
<II_II_BEFA_prev_img>:
    name: "befa_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "befa_r16_01.jpg"
                text: "[size=26]Buisness Economics And Financial Analysis (R16)[/size]"
                
            SmartTileWithLabel:
                source: "befa_r16_02.jpg"
                text: "[size=26]Buisness Economics And Financial Analysis (R16)[/size]"
                
            SmartTileWithLabel:
                source: "befa_r18_01.jpg"
                text: "[size=26]Buisness Economics And Financial Analysis (R18)[/size]"
                    
            SmartTileWithLabel:
                source: "befa_r18_02.jpg"
                text: "[size=26]Buisness Economics And Financial Analysis (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_II_subjects_img"
            
<II_II_DBMS_prev_img>:
    name: "dbms_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "dbms_r16_01.jpg"
                text: "[size=26]Database Management System (R16)[/size]"
                    
            SmartTileWithLabel:
                source: "dbms_r16_02.jpg"
                text: "[size=26]Database Management System (R18)[/size]"
                
            SmartTileWithLabel:
                source: "dbms_r18_01.jpg"
                text: "[size=26]Database Management System (R18)[/size]"
                
            SmartTileWithLabel:
                source: "dbms_r18_02.jpg"
                text: "[size=26]Database Management System (R18)[/size]" 
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_II_subjects_img"
            
<II_II_discrete_mathematics_prev_img>:
    name: "discrete_mathematics_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "dm_r16_01.jpg"
                text: "[size=26]Discrete Mathematics (R16)[/size]"
                
            SmartTileWithLabel:
                source: "dm_r16_02.jpg"
                text: "[size=26]Discrete Mathematics (R16)[/size]"
                
            SmartTileWithLabel:
                source: "dm_r18_01.jpg"
                text: "[size=26]Discrete Mathematics (R18)[/size]"
                
            SmartTileWithLabel:
                source: "dm_r18_02.jpg"
                text: "[size=26]Discrete Mathematics (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_II_subjects_img"
            
<II_II_java_programming_prev_img>:
    name: "java_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "java_r16_01.jpg"
                text: "[size=26]Java Programming (R16)[/size]"
                
            SmartTileWithLabel:
                source: "java_r16_02.jpg"
                text: "[size=26]Java Programming (R16)[/size]"
                
            SmartTileWithLabel:
                source: "java_r18_01.jpg"
                text: "[size=26]Java Programming (R18)[/size]"
                
            SmartTileWithLabel:
                source: "java_r18_02.jpg"
                text: "[size=26]Java Programming (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_II_subjects_img"
            
<II_II_operating_system_prev_img>:
    name: "operating_system_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
                
            SmartTileWithLabel:
                source: "os_r16_01.jpg"
                text: "[size=26]Operating System (R16)[/size]"
                
            SmartTileWithLabel:
                source: "os_r16_02.jpg"
                text: "[size=26]Operating System (R16)[/size]"
                    
            SmartTileWithLabel:
                source: "os_r18_01.jpg"
                text: "[size=26]Operating System (R18)[/size]"
                
            SmartTileWithLabel:
                source: "os_r18_02.jpg"
                text: "[size=26]Operating System (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "II_II_subjects_img"

"""

# year - III sem - I (pending!...)

questions_img_III_I = """
ScreenManager:
    III_I_subjects_img:
    III_I_computer_networks_prev_img:
    III_I_distributed_databases_prev_img:
    III_I_FLAT_prev_img:
    III_I_PPL_prev_img:
    III_I_SE_prev_img:
    III_I_WT_prev_img:
    

<III_I_subjects_img>:
    name: "III_I_subjects_img"
    MDRectangleFlatButton:
        text: "Computer Networks"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.9}
        on_press: root.manager.current = "cn_img"

    MDRectangleFlatButton:
        text: "Distributed Databases"
        font_size: '30sp'
        pos_hint: {"x": 0.33, "y": 0.75}
        on_press: root.manager.current = "dd_img"

    MDRectangleFlatButton:
        text: "Formal Languages And Automata Theory"
        font_size: '30sp'
        pos_hint: {"x": 0.18, "y": 0.6}
        on_press: root.manager.current = "flat_img"
    
    MDRectangleFlatButton:
        text: "Principle Of Programming Languages"
        font_size: '30sp'
        pos_hint: {"x": 0.22, "y": 0.45}
        on_press: root.manager.current = "ppl_img"
        
    MDRectangleFlatButton:
        text: "Software Engineering"
        font_size: '30sp'
        pos_hint: {"x": 0.32, "y": 0.3}
        on_press: root.manager.current = "se_img"
        
    MDRectangleFlatButton:
        text: "Web Technologies"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.15}
        on_press: root.manager.current = "wt_img"
        
    MDRectangleFlatButton:
        text: "Main Screen"
        font_size: '30sp'
        pos_hint: {"x": 0.17, "y": 0.15}
        on_press: app.restart()
        

<III_I_computer_networks_prev_img>:
    name: "cn_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "cn_r16_01.jpg"
                text: "[size=26]Computer Networks (R16)[/size]"
                
            SmartTileWithLabel:
                source: "cn_r16_02.jpg"
                text: "[size=26]Computer Networks (R16)[/size]"
                
            SmartTileWithLabel:
                source: "cn_r18_01.jpg"
                text: "[size=26]Computer Networks (R18)[/size]"
                    
            SmartTileWithLabel:
                source: "cn_r18_02.jpg"
                text: "[size=26]Computer Networks (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_I_subjects_img"
            
<III_I_distributed_databases_prev_img>:
    name: "dd_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "dd_r16_01.jpg"
                text: "[size=26]Distributed Database (R16)[/size]"
                
            SmartTileWithLabel:
                source: "dd_r16_02.jpg"
                text: "[size=26]Distributed Database (R16)[/size]"
                
            SmartTileWithLabel:
                source: "dd_r18_01.jpg"
                text: "[size=26]Distributed Database (R18)[/size]"
                
            SmartTileWithLabel:
                source: "dd_r18_02.jpg"
                text: "[size=26]Distributed Database (R18)[/size]"

                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_I_subjects_img"

<III_I_FLAT_prev_img>:
    name: "flat_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "flat_r16_01.jpg"
                text: "[size=26]Finite Languages And Automata Theory (R16)[/size]"
                
            SmartTileWithLabel:
                source: "flat_r16_02.jpg"
                text: "[size=26]Finite Languages And Automata Theory (R16)[/size]"
                
            SmartTileWithLabel:
                source: "flat_r18_01.jpg"
                text: "[size=26]Finite Languages And Automata Theory (R18)[/size]"
                    
            SmartTileWithLabel:
                source: "flat_r18_02.jpg"
                text: "[size=26]Finite Languages And Automata Theory (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_I_subjects_img"
            
<III_I_PPL_prev_img>:
    name: "ppl_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "ppl_r16_01.jpg"
                text: "[size=26]Principles Of Programming Languages (R16)[/size]"
                
            SmartTileWithLabel:
                source: "ppl_r16_02.jpg"
                text: "[size=26]Principles Of Programming Languages (R16)[/size]"
                
            SmartTileWithLabel:
                source: "ppl_r18_01.jpg"
                text: "[size=26]Principles Of Programming Languages (R18)[/size]"
            
            SmartTileWithLabel:
                source: "ppl_r18_02.jpg"
                text: "[size=26]Principles Of Programming Languages (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_I_subjects_img"
            
<III_I_SE_prev_img>:
    name: "se_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "se_r16_01.jpg"
                text: "[size=26]Software Engineering (R16)[/size]"
                
            SmartTileWithLabel:
                source: "se_r16_02.jpg"
                text: "[size=26]Software Engineering (R16)[/size]"
                
            SmartTileWithLabel:
                source: "se_r18_01.jpg"
                text: "[size=26]Software Engineering (R18)[/size]"
                
            SmartTileWithLabel:
                source: "se_r18_02.jpg"
                text: "[size=26]Software Engineering (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_I_subjects_img"

<III_I_WT_prev_img>:
    name: "wt_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "wt_r16_01.jpg"
                text: "[size=26]Web Technologies (R16)[/size]"
                
            SmartTileWithLabel:
                source: "wt_r16_02.jpg"
                text: "[size=26]Web Technologies (R16)[/size]"
                
            SmartTileWithLabel:
                source: "wt_r18_01.jpg"
                text: "[size=26]Web Technologies (R18)[/size]"
                
            SmartTileWithLabel:
                source: "wt_r18_02.jpg"
                text: "[size=26]Web Technologies (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_I_subjects_img"

"""

# year - III sem - II (pending...!)

questions_img_III_II = """
ScreenManager:
    III_II_subjects_img:
    III_II_machine_learning_prev_img:
    III_II_compiler_design_prev_img:
    III_II_DAA_prev_img:
    III_II_scripting_languages_prev_img:
    
<III_II_subjects_img>:
    name: "III_II_subjects_img"
    MDRectangleFlatButton:
        text: "Machine Learning"
        font_size: '30sp'
        pos_hint: {"x": 0.34, "y": 0.8}
        on_press: root.manager.current = "ml_img"

    MDRectangleFlatButton:
        text: "Compiler Design"
        font_size: '30sp'
        pos_hint: {"x": 0.35, "y": 0.6}
        on_press: root.manager.current = "cd_img"

    MDRectangleFlatButton:
        text: "Design Analysis and Algorithms"
        font_size: '30sp'
        pos_hint: {"x": 0.25, "y": 0.4}
        on_press: root.manager.current = "daa_img"
    
    MDRectangleFlatButton:
        text: "Scripting Languages"
        font_size: '30sp'
        pos_hint: {"x": 0.32, "y": 0.2}
        on_press: root.manager.current = "sl_img"
        
    MDRectangleFlatButton:
        text: "Main Screen"
        font_size: '30sp'
        pos_hint: {"x": 0.1, "y": 0.2}
        on_press: app.restart()

<III_II_machine_learning_prev_img>:
    name: "ml_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "ml_r16_01.jpg"
                text: "[size=26]Machine Learning (R16)[/size]"
                
            SmartTileWithLabel:
                source: "ml_r16_02.jpg"
                text: "[size=26]Machine Learning (R16)[/size]"
                
            SmartTileWithLabel:
                source: "ml_r18_01.jpg"
                text: "[size=26]Machine Learning (R18)[/size]"
                
            SmartTileWithLabel:
                source: "ml_r18_02.jpg"
                text: "[size=26]Machine Learning (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_II_subjects_img"

<III_II_compiler_design_prev_img>:
    name: "cd_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "cd_r16_01.jpg"
                text: "[size=26]Compiler Design (R16)[/size]"
                
            SmartTileWithLabel:
                source: "cd_r16_02.jpg"
                text: "[size=26]Compiler Design (R16)[/size]"
                
            SmartTileWithLabel:
                source: "cd_r18_01.jpg"
                text: "[size=26]Compiler Design (R18)[/size]"
                    
            SmartTileWithLabel:
                source: "cd_r18_02.jpg"
                text: "[size=26]Compiler Design (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_II_subjects_img"

<III_II_DAA_prev_img>:
    name: "daa_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "daa_r16_01.jpg"
                text: "[size=26]Design And Analysis Of Algorithms (R16)[/size]"
                
            SmartTileWithLabel:
                source: "daa_r16_02.jpg"
                text: "[size=26]Design And Analysis Of Algorithms (R16)[/size]"
                
            SmartTileWithLabel:
                source: "daa_r18_01.jpg"
                text: "[size=26]Design And Analysis Of Algorithms (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_II_subjects_img"

<III_II_scripting_languages_prev_img>:
    name: "sl_img"
    ScrollView:
        MDGridLayout:        
            cols: 1
            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
            row_force_default: True
            adaptive_height: True
            padding: dp(60), dp(10)
            spacing: dp(5)
            
            SmartTileWithLabel:
                source: "sl_r18_01.jpg"
                text: "[size=26]Scripting Languages (R18)[/size]"
                
            SmartTileWithLabel:
                source: "sl_r18_02.jpg"
                text: "[size=26]Scripting Languages (R18)[/size]"
                    
            MDRectangleFlatButton:
                text: "Back"
                font_size: "25sp"
                pos_hint: {"x": 0.2, "y": 0.2}
                on_press: root.manager.current = "III_II_subjects_img"

"""


