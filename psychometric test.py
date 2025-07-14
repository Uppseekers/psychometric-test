import streamlit as st
import time
import base64
from io import BytesIO
from PIL import Image

# --- Configuration ---
TEST_DURATION_SECONDS = 600  # 10 minutes for the whole test
NUM_QUESTIONS = 10

# --- Helper Function to create a simple image (replace with actual image files) ---
def create_abstract_image(description):
    """
    This is a placeholder. In a real app, you would load pre-designed images
    from a 'images' folder or use a library like Pillow to draw them.
    For this example, we'll create a simple placeholder image or
    encode a text description as an image.
    """
    try:
        # Attempt to create a simple image using Pillow (Pillow must be installed)
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (300, 150), color = (255, 255, 255)) # White background
        d = ImageDraw.Draw(img)
        
        # Load a default font if available, or use a basic one
        try:
            fnt = ImageFont.truetype("arial.ttf", 20) # Adjust path as needed
        except IOError:
            fnt = ImageFont.load_default()

        # Split description to fit
        words = description.split()
        lines = []
        current_line = []
        for word in words:
            if d.textlength(" ".join(current_line + [word]), font=fnt) < 280: # Max width for text
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        
        y_text = 20
        for line in lines:
            d.text((10, y_text), line, fill=(0,0,0), font=fnt)
            y_text += 25

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return buffered.getvalue()
    except ImportError:
        st.warning("Pillow not installed. Displaying text description instead of image.")
        return description.encode('utf-8') # Fallback to bytes of text if Pillow is not there


# --- Test Questions Data ---
# In a real application, you would reference image paths or base64 encoded images.
# For simplicity, I'm using descriptive strings that create simple images.
questions_data = [
    {
        "type": "Series Completion",
        "prompt_images": [
            "White square, small black circle top-left",
            "White square, small black circle top-right",
            "White square, small black circle bottom-right"
        ],
        "options": [
            "White square, small black circle top-left",
            "White square, small black circle top-right",
            "White square, small black circle bottom-left",
            "White square, small black circle bottom-right"
        ],
        "correct_answer": "White square, small black circle bottom-left",
        "logic_explanation": "The small black circle moves clockwise around the corners of the square."
    },
    {
        "type": "Series Completion",
        "prompt_images": [
            "Large black circle, 1 small white dot",
            "Large black circle, 2 small white dots",
            "Large black circle, 3 small white dots"
        ],
        "options": [
            "Large black circle, 2 small white dots",
            "Large black circle, 3 small white dots",
            "Large black circle, 4 small white dots",
            "Large black circle, 5 small white dots"
        ],
        "correct_answer": "Large black circle, 4 small white dots",
        "logic_explanation": "The number of small white dots inside the circle is increasing by one in each step."
    },
    {
        "type": "Odd One Out",
        "prompt_images": [
            "Three vertical parallel lines",
            "Three horizontal parallel lines",
            "Three diagonal parallel lines (TL-BR)",
            "Two vertical parallel lines"
        ],
        "options_are_images": True, # Indicates options are the images themselves
        "correct_answer": "Two vertical parallel lines",
        "logic_explanation": "All options except the correct one consist of three lines. The correct one has only two lines."
    },
    {
        "type": "Odd One Out",
        "prompt_images": [
            "Solid black triangle pointing upwards",
            "Solid black triangle pointing downwards",
            "Solid black triangle pointing right",
            "Hollow white triangle pointing upwards"
        ],
        "options_are_images": True,
        "correct_answer": "Hollow white triangle pointing upwards",
        "logic_explanation": "All options except the correct one are solid black triangles. The correct one is a hollow white triangle."
    },
    {
        "type": "Matrix Reasoning",
        "prompt_images": [
            "Row 1: 1 Circle, 2 Circles, 3 Circles",
            "Row 2: 1 Square, 2 Squares, 3 Squares",
            "Row 3: 1 Triangle, 2 Triangles, ?"
        ],
        "options": [
            "1 Triangle", "2 Triangles", "3 Triangles", "4 Triangles"
        ],
        "correct_answer": "3 Triangles",
        "logic_explanation": "In each row, the number of shapes increases by one from left to right (1, 2, 3)."
    },
    {
        "type": "Matrix Reasoning",
        "prompt_images": [
            "Row 1: Black circle, Black square, Black triangle",
            "Row 2: White circle, White square, White triangle",
            "Row 3: Grey circle, Grey square, ?"
        ],
        "options": [
            "Black triangle", "White triangle", "Grey triangle", "Grey circle"
        ],
        "correct_answer": "Grey triangle",
        "logic_explanation": "Horizontally, the shape changes (circle -> square -> triangle). Vertically, the color remains constant. The missing figure is a Grey Triangle."
    },
    {
        "type": "Series Completion",
        "prompt_images": [
            "Square with 'X' inside",
            "Square with '+' inside",
            "Square with 'X' inside"
        ],
        "options": [
            "Square with 'X' inside",
            "Square with '+' inside",
            "Square with circle inside",
            "Square with no symbol"
        ],
        "correct_answer": "Square with '+' inside",
        "logic_explanation": "The pattern is an alternating sequence: 'X', '+', 'X', '+'."
    },
    {
        "type": "Advanced Series Completion",
        "prompt_images": [
            "Large circle, small square inside",
            "Large square, small circle inside",
            "Large triangle, small square inside"
        ],
        "options": [
            "Large triangle, small circle inside",
            "Large square, small triangle inside",
            "Large circle, small triangle inside",
            "Large circle, small square inside"
        ],
        "correct_answer": "Large triangle, small circle inside",
        "logic_explanation": "The outer shape progresses alphabetically (Circle, Square, Triangle). The inner shape alternates between Circle and Square. So, the next outer shape is a Triangle, and the next inner shape is a Circle."
    },
    {
        "type": "Visual Analogy",
        "prompt_images": [
            "Relationship 1: Square IS TO Square with vertical line",
            "Relationship 2: Circle IS TO ?"
        ],
        "options": [
            "Circle with horizontal line",
            "Circle with vertical line",
            "Circle with 'X' inside",
            "Circle with no line"
        ],
        "correct_answer": "Circle with vertical line",
        "logic_explanation": "The relationship is that a vertical line is added to the figure. This same transformation must be applied to the Circle."
    },
    {
        "type": "Visual Analogy",
        "prompt_images": [
            "Relationship 1: Large square enclosing small circle IS TO Large circle enclosing small square",
            "Relationship 2: Large triangle enclosing small star IS TO ?"
        ],
        "options": [
            "Large star enclosing small triangle",
            "Large triangle enclosing small star",
            "Large triangle enclosing small circle",
            "Large star enclosing large triangle"
        ],
        "correct_answer": "Large star enclosing small triangle",
        "logic_explanation": "The relationship is that the outer shape and inner shape swap positions and roles. Applying this, the outer triangle and inner star should swap."
    }
]

# --- Initialize Session State ---
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.start_time = None
    st.session_state.answers = {} # To store user answers
    st.session_state.quiz_completed = False

# --- UI Layout ---
st.set_page_config(layout="wide", page_title="Pattern Seeker Challenge")

st.title("🧠 Pattern Seeker Challenge")
st.markdown("---")

if not st.session_state.quiz_started:
    st.info("Welcome to the Pattern Seeker Challenge! This test assesses your Logical and Abstract Reasoning skills by identifying patterns in visual sequences. You will have 10 minutes to complete 10 questions.")
    st.warning(f"**Important:** Once you start, the timer begins. Do not refresh the page.")
    if st.button("Start Quiz"):
        st.session_state.quiz_started = True
        st.session_state.start_time = time.time()
        st.rerun() # Rerun to immediately show the first question

elif st.session_state.quiz_completed:
    st.success("🎉 Quiz Completed!")
    st.write(f"You scored: **{st.session_state.score} out of {NUM_QUESTIONS}**")
    st.write("Thank you for completing the test. Your detailed results and insights will be provided soon.")

    if st.button("Review Answers"):
        st.subheader("Your Answers vs. Correct Answers")
        for i, q_data in enumerate(questions_data):
            st.markdown(f"---")
            st.markdown(f"**Question {i+1}: {q_data['type']}**")
            
            # Display prompt images
            cols = st.columns(len(q_data["prompt_images"]))
            for j, img_desc in enumerate(q_data["prompt_images"]):
                with cols[j]:
                    st.image(create_abstract_image(img_desc), caption=f"Prompt {j+1}", use_column_width=True)

            user_answer = st.session_state.answers.get(i, "Not answered")
            correct_answer = q_data["correct_answer"]
            
            st.write(f"**Your Answer:** {user_answer}")
            st.write(f"**Correct Answer:** {correct_answer}")
            
            if user_answer == correct_answer:
                st.markdown("✅ **Correct!**")
            else:
                st.markdown("❌ **Incorrect.**")
            
            st.info(f"**Logic:** {q_data['logic_explanation']}")
    
    if st.button("Restart Quiz"):
        # Reset all session state variables
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

else:
    current_time = time.time()
    elapsed_time = current_time - st.session_state.start_time
    remaining_time = max(0, TEST_DURATION_SECONDS - elapsed_time)

    # --- Timer Display ---
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    timer_placeholder = st.empty()
    timer_placeholder.markdown(f"⏰ Time Remaining: **{minutes:02d}:{seconds:02d}**")

    if remaining_time <= 0:
        st.session_state.quiz_completed = True
        st.warning("Time's up! The quiz has ended.")
        st.rerun() # Trigger a rerun to show completion message

    # --- Display Current Question ---
    if st.session_state.current_question_idx < NUM_QUESTIONS:
        q_idx = st.session_state.current_question_idx
        question = questions_data[q_idx]

        st.subheader(f"Question {q_idx + 1} of {NUM_QUESTIONS}: {question['type']}")
        st.markdown("---")

        # Display prompt images for the question
        cols = st.columns(len(question["prompt_images"]))
        for j, img_desc in enumerate(question["prompt_images"]):
            with cols[j]:
                st.image(create_abstract_image(img_desc), caption=f"Figure {j+1}", use_column_width=True)

        st.markdown("---")

        # Display options
        # For 'Odd One Out', the prompt_images are also the options, so we handle that specifically
        if question.get("options_are_images", False):
            selected_option = st.radio(
                "Which one is the Odd One Out?",
                options=question["prompt_images"],
                key=f"q{q_idx}_option"
            )
        else:
            selected_option = st.radio(
                "Select the correct option:",
                options=question["options"],
                key=f"q{q_idx}_option"
            )

        # --- Navigation Buttons ---
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Previous", disabled=(q_idx == 0)):
                st.session_state.answers[q_idx] = selected_option # Save current answer
                st.session_state.current_question_idx -= 1
                st.rerun()

        with col2:
            if st.button("Next"):
                # Process answer
                st.session_state.answers[q_idx] = selected_option
                if selected_option == question["correct_answer"]:
                    st.session_state.score += 1
                
                # Move to next question or complete quiz
                if st.session_state.current_question_idx < NUM_QUESTIONS - 1:
                    st.session_state.current_question_idx += 1
                else:
                    st.session_state.quiz_completed = True
                st.rerun()
    else:
        st.session_state.quiz_completed = True
        st.rerun()

