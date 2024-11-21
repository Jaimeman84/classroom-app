import streamlit as st
import time
import random
from name_picker import NamePicker
from group_generator import GroupGenerator
import pandas as pd
import json

def load_animations():
    """Load CSS animations"""
    st.markdown("""
        <style>
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
            40% {transform: translateY(-30px);}
            60% {transform: translateY(-15px);}
        }
        @keyframes spin {
            0% {transform: rotate(0deg);}
            100% {transform: rotate(360deg);}
        }
        .bounce {
            animation: bounce 1s infinite;
        }
        .spin {
            animation: spin 1s infinite;
        }
        .stButton>button {
            background-color: #1e88e5;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: ##1e88e5;
            transform: scale(1.05);
        }
        .student-card {
            background-color: #1e88e5;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        .student-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .group-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 10px;
        }
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background-color: #f0f0f0;
            animation: fall 3s ease-in infinite;
        }
        @keyframes fall {
            to {
                transform: translateY(100vh);
            }
        }
        </style>
    """, unsafe_allow_html=True)

def create_confetti():
    """Create confetti effect"""
    confetti = ""
    for i in range(50):
        color = random.choice(['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'])
        left = random.randint(0, 100)
        delay = random.random() * 3
        confetti += f"""
            <div class="confetti" style="left: {left}vw; 
                                       background-color: {color}; 
                                       animation-delay: {delay}s;">
            </div>
        """
    st.markdown(confetti, unsafe_allow_html=True)

def display_student_card(name, color):
    """Display a student card with animation"""
    st.markdown(f"""
        <div class="student-card" style="background-color: {color}">
            <h3 style="color: white; text-align: center;">{name}</h3>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Interactive Classroom Helper", layout="wide")
    load_animations()
    
    # Custom title with emoji
    st.markdown("""
        <h1 style='text-align: center; color: #1e88e5;'>
            🎓 Interactive Classroom Helper 🎨
        </h1>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'name_picker' not in st.session_state:
        st.session_state.name_picker = NamePicker()
    if 'group_generator' not in st.session_state:
        st.session_state.group_generator = GroupGenerator()
    if 'picked_history' not in st.session_state:
        st.session_state.picked_history = []
    
    tab1, tab2 = st.tabs(["✨ Name Picker", "👥 Group Generator"])
    
    with tab1:
        st.markdown("""
            <h2 style='text-align: center;'>
                Magic Name Picker 🎯
            </h2>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            names_input = st.text_area(
                "✏️ Enter student names (one per line)",
                height=150,
                placeholder="John Smith\nJane Doe\n..."
            )
            
            if st.button("➕ Add Names", key="add_names"):
                names_list = [name.strip() for name in names_input.split('\n') if name.strip()]
                st.session_state.name_picker.add_names(names_list)
                st.success("🎉 Names added successfully!")

            if st.button("🎲 Pick Random Name!", key="pick_name"):
                if st.session_state.name_picker.names:
                    with st.spinner("🔮 Making a magical selection..."):
                        placeholder = st.empty()
                        
                        # Animated selection effect
                        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD']
                        for _ in range(15):
                            temp_name = random.choice(st.session_state.name_picker.names)
                            color = random.choice(colors)
                            with placeholder:
                                display_student_card(temp_name, color)
                            time.sleep(0.2)
                        
                        final_name = st.session_state.name_picker.pick_random_name()
                        create_confetti()
                        with placeholder:
                            display_student_card(final_name, '#1e88e5')
                        
                        st.session_state.picked_history.append(final_name)
                        
                        # Show celebration message
                        st.balloons()
                        st.success(f"🌟 Congratulations {final_name}! 🌟")
                else:
                    st.warning("⚠️ Please add some names first!")

            # Show picking history
            if st.session_state.picked_history:
                st.markdown("### 📚 Selection History")
                history_df = pd.DataFrame({"Selected Students": st.session_state.picked_history})
                st.dataframe(history_df, use_column_width=True)  

        with col2:
            st.markdown("### 📝 Current List")
            if st.session_state.name_picker.names:
                for name in st.session_state.name_picker.names:
                    st.markdown(f"- {name}")



    with tab2:
        st.markdown("""
            <h2 style='text-align: center;'>
                Group Generator 🎨
            </h2>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            students_input = st.text_area(
                "✏️ Enter student names (one per line)",
                height=150,
                key="group_students",
                placeholder="John Smith\nJane Doe\n..."
            )

        with col2:
            num_groups = st.number_input(
                "🔢 Number of groups",
                min_value=1,
                value=2,
                help="Choose how many groups to create"
            )
            
            group_theme = st.selectbox(
                "🎨 Select Group Theme",
                ["Colors", "Animals", "Superheroes", "Countries"]
            )

        if st.button("🎯 Generate Groups!", key="generate_groups"):
            students_list = [name.strip() for name in students_input.split('\n') if name.strip()]
            if students_list:
                st.session_state.group_generator.set_students(students_list)
                groups = st.session_state.group_generator.generate_groups(num_groups)
                
                # Theme-based group names
                themes = {
                    "Colors": ["Red Stars", "Blue Dragons", "Green Phoenix", "Yellow Lions", "Purple Knights"],
                    "Animals": ["Tigers", "Eagles", "Dolphins", "Panthers", "Bears"],
                    "Superheroes": ["Avengers", "Justice League", "Guardians", "X-Men", "Defenders"],
                    "Countries": ["Japan", "Brazil", "India", "Italy", "Canada"]
                }
                
                with st.spinner("🎨 Creating colorful groups..."):
                    time.sleep(1)
                    st.balloons()
                    
                    # Display groups in a grid
                    cols = st.columns(len(groups))
                    for i, (col, group) in enumerate(zip(cols, groups)):
                        with col:
                            group_name = themes[group_theme][i % len(themes[group_theme])]
                            st.markdown(f"""
                                <div class='group-container' style='background-color: {random.choice(['#e3f2fd', '#f3e5f5', '#e8f5e9', '#fff3e0'])}'>
                                    <h3 style='text-align: center; color: #1976d2;'>
                                        {group_name}
                                    </h3>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            for student in group:
                                st.markdown(f"""
                                    <div class='student-card' style='text-align: center;'>
                                        👤 {student}
                                    </div>
                                """, unsafe_allow_html=True)
                
                # Add export functionality
                if st.button("📥 Export Groups"):
                    export_data = {
                        f"Group {i+1} - {themes[group_theme][i % len(themes[group_theme])]}": group
                        for i, group in enumerate(groups)
                    }
                    st.download_button(
                        "Download Groups (JSON)",
                        data=json.dumps(export_data, indent=2),
                        file_name="groups.json",
                        mime="application/json"
                    )
            else:
                st.warning("⚠️ Please add some student names first!")

if __name__ == "__main__":
    main()