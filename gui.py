import tkinter as tk

import calc


class GUI(tk.Tk):
    """A simple Tk-based interface for real-time entropy-related analytics
    on given texts."""

    def __init__(self):
        """Initializes the GUI where 'root' is a tkinter.Tk instance."""
        super().__init__()
        self.state("zoomed")

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nwes")

        self.input_head = tk.Label(self.frame, text="Input:")
        self.input_head.grid(row=0, column=0, sticky="nwes")
        self.ignore_case_value = tk.IntVar()
        self.ignore_case_value.trace("w", self.case_switch)
        self.ignore_case = tk.Checkbutton(
            self.frame,
            variable=self.ignore_case_value,
            text="Ignore case"
        )
        self.ignore_case.grid(row=0, column=1, sticky="nwes")
        self.input_main = tk.Text(self.frame)
        self.input_main.grid(row=1, column=0, sticky="nwes", columnspan=2)
        self.input_main.bind("<KeyRelease>", self.update)

        self.output_head = tk.Label(self.frame, text="Output:")
        self.output_head.grid(row=0, column=2, sticky="nwes")
        self.output_main = tk.Text(self.frame, state=tk.DISABLED)
        self.output_main.grid(row=1, column=2, sticky="nwes")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

    def case_switch(self, *_):
        """Toggles case sensivity."""
        self.input_main.edit_modified(True)
        self.update()

    def update(self, *_):
        """Updates the contents of the analysis text box."""
        if not self.input_main.edit_modified():
            return

        analyze_text = self.create_analysis()
        self.output_main["state"] = tk.NORMAL
        self.output_main.delete("1.0", tk.END)
        self.output_main.insert("1.0", analyze_text)
        self.output_main["state"] = tk.DISABLED
        self.input_main.edit_modified(False)

    def create_analysis(self):
        """Creates the analysis text."""
        text = self.input_main.get("1.0", "end-1c")
        if not text:
            return ""
        if self.ignore_case_value.get():
            text = text.lower()

        char_map = calc.char_mapping(text)
        unique_chars = len(char_map)
        entropy = calc.entropy(text)
        metric_entropy = calc.metric_entropy(text)
        optimal = calc.optimal_bits(text)

        info = """Length: {}
Unique chars: {}
Entropy: {}
Metric entropy: {}
Optimal bit usage: {}""".format(
            len(text),
            unique_chars,
            entropy,
            metric_entropy,
            optimal
        )

        table_head = " Char | Probability |     Bits    | Occurrences "
        table_body = "\n".join(
            [
                " {:<4} | {:>11.7f} | {:>11.7f} | {:>11}".format(
                    char,
                    prob, calc.prob_to_info(prob),
                    text.count(char)
                )
                for char, prob in char_map
            ]
        )
        table = "\n".join([table_head, table_body])

        return "\n\n".join([info, table])

if __name__ == "__main__":
    root = GUI()
    root.mainloop()
