import tkinter as tk

import calc


class GUI:
    def __init__(self, root):
        self.parent = root
        self.parent.state("zoomed")

        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nwes")

        self.input_head = tk.Label(self.frame, text="Input:")
        self.input_head.grid(row=0, column=0, sticky="nwes")
        self.ignore_case_value = tk.IntVar()
        self.ignore_case_value.trace("w", self.case_switch)
        self.ignore_case = tk.Checkbutton(self.frame,
                                          variable=self.ignore_case_value,
                                          text="Ignore case")
        self.ignore_case.grid(row=0, column=1, sticky="nwes")
        self.input_main = tk.Text(self.frame)
        self.input_main.grid(row=1, column=0, sticky="nwes", columnspan=2)
        self.input_main.bind("<KeyRelease>", self.update)

        self.output_head = tk.Label(self.frame, text="Output:")
        self.output_head.grid(row=0, column=2, sticky="nwes")
        self.output_main = tk.Text(self.frame, state=tk.DISABLED)
        self.output_main.grid(row=1, column=2, sticky="nwes")

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

    def case_switch(self, *_):
        self.input_main.edit_modified(True)
        self.update()

    def update(self, *_):
        if self.input_main.edit_modified():
            text = self.calculate()
            self.output_main["state"] = tk.NORMAL
            self.output_main.delete("1.0", tk.END)
            self.output_main.insert("1.0", text)
            self.output_main["state"] = tk.DISABLED
            self.input_main.edit_modified(False)

    def calculate(self, *_):
        text = self.input_main.get("1.0", "end-1c")
        if self.ignore_case_value.get():
            text = text.lower()
        char_map = calc.char_mapping(text)

        entropy = calc.entropy(char_map)
        metric_entropy = calc.metric_entropy(entropy, len(text))
        optimal = calc.optimal_bits(entropy, len(text))

        info = "\n".join(
            [
                "Length: " + str(len(text)),
                "Unique chars: " + str(len(char_map)),
                "Entropy: " + str(entropy),
                "Metric entropy: " + str(metric_entropy),
                "Optimal bit usage: " + str(optimal)
            ]
        )

        table_head = " Char\t| Probability\t\t| Bits\t\t| Occurences"
        table_body = "\n".join(
            [
                " " + repr(char)[1:-1] +
                "\t" + str(round(prob, 7)) +
                "\t\t" + str(round(calc.prob_to_info(prob), 7)) +
                "\t\t" + str(text.count(char))
                for char, prob in char_map
            ]
        )
        table = "\n".join([table_head, table_body])

        return "\n\n".join([info, table])


def main():
    root = tk.Tk()
    _ = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
