from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        friends_raw = request.form['friends']
        friends = [f.strip() for f in friends_raw.split(',') if f.strip()]
        mode = request.form.get('mode')
        bill_amount = request.form.get('bill_amount', type=float)
        split_count = request.form.get('split_count', type=int)

        if not friends:
            result = "⚠️ Please enter at least one name."
        elif mode == 'random':
            chosen = random.choice(friends)
            result = f"🎉 {chosen} has been selected to pay the entire bill!"
        elif mode == 'split':
            if not split_count or split_count < 1:
                result = "⚠️ Please enter a valid number of people to split the bill."
            elif split_count > len(friends):
                result = "⚠️ You can't split the bill among more people than are listed."
            else:
                selected = random.sample(friends, split_count)
                if bill_amount:
                    if split_count == 1:
                        result = f"💸 {selected[0]} will pay the entire bill of ₦{bill_amount:,.2f}."
                    else:
                        share = round(bill_amount / split_count, 2)
                        result = f"💸 The bill will be split among {', '.join(selected)}. Each pays ₦{share:,.2f}."
                else:
                    if split_count == 1:
                        result = f"🧾 {selected[0]} will pay the full bill."
                    else:
                        result = f"🧾 The bill will be split among: {', '.join(selected)}."
        else:
            result = "⚠️ Invalid mode selected."

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
