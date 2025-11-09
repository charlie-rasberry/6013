#   TODO:   Refactor,especially change expected names as I jumped the gun when first making this without sampling properly
#   TODO:   Add button labels and finalise the categories of aspects
#   TODO:   Ensure there is persistent progress tracking implentation before labelling 
#   TODO:   Finalise keybinds
#   TODO:   Display progress    e.g. review 1020 of 5000
#   TODO:   Validate saving progres
#   TODO:   Loop instead of pressing enter
#   TODO:   Autosave ? / confirm quit at least
#   TODO:   More visual q's


import tkinter as tk
from tkinter import ttk
import pandas as pd

"""
app to classify / manually annotate reviews for ml training
currently has hotkeys for each option 1 0 asdfghjkl
path must be to tagged not sampled, it wont remember
"""


class MultiTag:
    def __init__(self):
        self.root = tk.Tk()
        # root.geometry("400x300")
        self.active_column = 0  # used for highlighting the current column 
        self.btn_width = 15 # button width
        self.number_of_aspects = 9  # number of aspect buttons
        self.root.title("MultiTag")

        self.display_review = tk.Text(self.root, height=20, width=100, wrap='word')
        self.display_review.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # highlight for the current box
        self.highlight = tk.Frame(self.root, bg="#003366", height=20, width=130)
        self.highlight.grid(row=11, column=0)


        #   Labels
        ttk.Label(self.root, text="Feature Request ? 1 (yes), 0 (no)").grid(row= 1, column=0)
        ttk.Label(self.root, text="Bug Report ? 1 (yes), 0 (no)").grid(row= 1, column=1)
        ttk.Label(self.root, text="Aspect ? A/S/D/F/G/H/J/K/L ").grid(row= 1, column=2)
        ttk.Label(self.root, text="Aspect Sentiment ? A/S/D").grid(row= 1, column=3)


        self.feature_true = ttk.Button(self.root, text="1",command=lambda: self.feature_pressed("1"), width= self.btn_width).grid(row=2, column=0)
        self.feature_false = ttk.Button(self.root, text="0",command=lambda: self.feature_pressed("0"), width= self.btn_width).grid(row=3, column=0)

        self.bug_true = ttk.Button(self.root, text="1",command=lambda: self.bug_pressed("1"), width= self.btn_width).grid(row = 2, column=1)
        self.bug_false = ttk.Button(self.root, text="0",command=lambda: self.bug_pressed("0"), width= self.btn_width).grid(row = 3, column=1)

        self.aspect_a = ttk.Button(self.root, text="A: ASPECT HERE",command=lambda: self.aspect_pressed("A"), width= self.btn_width).grid(row = 2, column=2)
        self.aspect_s = ttk.Button(self.root, text="S: ASPECT HERE", command=lambda: self.aspect_pressed("S"), width= self.btn_width).grid(row = 3, column=2)
        self.aspect_d = ttk.Button(self.root, text="D: ASPECT HERE", command=lambda: self.aspect_pressed("D"), width= self.btn_width).grid(row = 4, column=2)
        self.aspect_f = ttk.Button(self.root, text="F: ASPECT HERE", command=lambda: self.aspect_pressed("F"), width= self.btn_width).grid(row = 5, column=2)
        self.aspect_g = ttk.Button(self.root, text="G: ASPECT HERE", command=lambda: self.aspect_pressed("G"), width= self.btn_width).grid(row = 6, column=2)
        self.aspect_h = ttk.Button(self.root, text="H: ASPECT HERE", command=lambda: self.aspect_pressed("H"), width= self.btn_width).grid(row = 7, column=2)
        self.aspect_j = ttk.Button(self.root, text="J: ASPECT HERE", command=lambda: self.aspect_pressed("J"), width= self.btn_width).grid(row = 8, column=2)
        self.aspect_k = ttk.Button(self.root, text="K: ASPECT HERE", command=lambda: self.aspect_pressed("K"), width= self.btn_width).grid(row = 9, column=2)
        self.aspect_l = ttk.Button(self.root, text="L: ASPECT HERE", command=lambda: self.aspect_pressed("L"), width= self.btn_width).grid(row = 10, column=2)

        self.aspect_positive = ttk.Button(self.root, text="A: Positive", command=lambda: self.sentiment_pressed("A"), width= self.btn_width).grid(row=2, column=3)
        self.aspect_neutral = ttk.Button(self.root, text="S: Neutral", command=lambda: self.sentiment_pressed("S"), width= self.btn_width).grid(row=3, column=3)
        self.aspect_negative = ttk.Button(self.root, text="D: Negative", command=lambda: self.sentiment_pressed("D"), width= self.btn_width).grid(row=4, column=3)

        #   keys
        self.root.bind("q", self.quit_app)
        self.root.bind("<Return>", self.try_submit)
        self.root.bind("1", self.handle_key)
        self.root.bind("0", self.handle_key)
        self.root.bind("a", self.handle_key)
        self.root.bind("s", self.handle_key)
        self.root.bind("d", self.handle_key)
        self.root.bind("f", self.handle_key)
        self.root.bind("g", self.handle_key)
        self.root.bind("h", self.handle_key)
        self.root.bind("j", self.handle_key)
        self.root.bind("k", self.handle_key)
        self.root.bind("l", self.handle_key)

        
        self.load_review_data("data/uber_reviews_sampled.csv")
        # self.load_review_data("data/uber_reviews_tagged.csv")

        self.display_next_review()
        #   self.save_tags("data/uber_reviews_tagged.csv")

        self.root.mainloop()

    def handle_key(self, event):
        key = event.char
    
        # Column 0 or 1: feature/bug (1 and 0)
        if key in ['1', '0']:
            if self.active_column == 0:
                self.feature_pressed(key)
            elif self.active_column == 1:
                self.bug_pressed(key)
        # Column 2: aspects (a,s,d,f,g,h,j,k,l)
        elif key in 'asdfghjkl' and self.active_column == 2:
            self.aspect_pressed(key.upper())
        # Column 3: sentiment (a,s,d)
        elif key in 'asd' and self.active_column == 3:
            self.sentiment_pressed(key.upper())
    
    def move_highlight(self, row, col):
        """Move the highlight box directly under the button pressed."""
        self.highlight.grid(row=row, column=col)
        self.highlight.grid()  # make sure it’s visible


    def feature_pressed(self, value):
        self.review_data.at[self.current_review_index, "feature_request"] = value
        self.active_column = 1
        self.move_highlight(self.number_of_aspects + 2, 1)

    def bug_pressed(self, value):
        self.review_data.at[self.current_review_index, "bug_report"] = value
        self.active_column = 2
        self.move_highlight(self.number_of_aspects + 2, 2)

    def aspect_pressed(self, value):
        self.review_data.at[self.current_review_index, "aspect"] = value
        self.active_column = 3
        self.move_highlight(self.number_of_aspects + 2, 3)

    def sentiment_pressed(self, value):
        self.review_data.at[self.current_review_index, "aspect_sentiment"] = value
        self.active_column = 0  # Reset for next review


    def load_review_data(self, data_path):
        """Load review data from a CSV file."""
        self.review_data = pd.read_csv(data_path, low_memory=False)
        if "tagged" not in self.review_data.columns:
            self.review_data["tagged"] = 0  # Initialize tagged column if not present
        if "feature_request" not in self.review_data.columns:
            self.review_data["feature_request"] = ""  # Initialize feature_request column if not present
        if "bug_report" not in self.review_data.columns:
            self.review_data["bug_report"] = ""  # Initialize bug_report column if not present
        if "aspect" not in self.review_data.columns:
            self.review_data["aspect"] = ""  # Initialize aspect column if not present
        if "aspect_sentiment" not in self.review_data.columns:
            self.review_data["aspect_sentiment"] = ""  # Initialize aspect_sentiment column if not present
        print(f"Loaded {len(self.review_data)} reviews from {data_path}")
    
    def display_next_review(self):
        """Display the next review in the text box."""
        self.current_review_index = self.get_current_review_index()
        if self.current_review_index < len(self.review_data):
            review = self.review_data.iloc[self.current_review_index]
            self.display_review.delete(1.0, tk.END)  # Clear the text box
            self.display_review.insert(tk.END, review["review_description"])  # Display the review text
            # self.current_review_index += 1
            # Mark as tagged
            #   self.review_data.at[self.current_review_index - 1, "tagged"] = 1
            self.active_column = 0  # reset to start at feature request
            self.move_highlight(self.number_of_aspects + 2, 0)
            
        else:
            print("No more reviews to display.")

    def submit_tag(self):
        self.review_data.at[self.current_review_index, "tagged"] = 1
        self.save_tags("data/uber_reviews_tagged.csv")
        self.display_next_review()

    def try_submit(self, event):
        """Try to submit current review if all labels complete."""
        if self.all_labels_complete():
            self.submit_tag()
            self.move_highlight(self.number_of_aspects + 2, 0)

            print("Labels submitted, loading next review")
        else:
            print("Please complete all labels before submitting")
    
    def all_labels_complete(self):
        row = self.review_data.iloc[self.current_review_index]
        return (row["feature_request"] != "" and 
            row["bug_report"] != "" and 
            row["aspect"] != "" and 
            row["aspect_sentiment"] != "")
    
    def save_tags(self, save_path):
        """Save the tagged data to a CSV file."""
        self.review_data.to_csv(save_path, index=False)
        print(f"Tagged data saved to {save_path}")

    def quit_app(self, event):
        self.root.destroy()
        self.save_tags("data/uber_reviews_tagged.csv")

    def get_current_review_index(self):
        for i in range(len(self.review_data)):
            if self.review_data.iloc[i]["tagged"] == 0:
                return i
        return self.review_data.shape[0]  # all reviews tagged
    
    
    
app = MultiTag()
