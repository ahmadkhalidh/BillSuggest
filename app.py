from flask import Flask, render_template, request
import random
import math

app = Flask(__name__)

def random_split(bill_amount, friends, count):
    selected = random.sample(friends, count)  # Pick exact number of friends

    # Generate random weights
    weights = [random.random() for _ in range(count)]
    total_weight = sum(weights)

    # Split amounts (rounded up to whole Naira)
    raw_shares = [(bill_amount * w / total_weight) for w in weights]
    shares = [math.ceil(share) for share in raw_shares]

    # Adjust the last person's share to fix any over-rounding
    total_share = sum(shares)
    excess = total_share - bill_amount
    shares[-1] -= excess

    return dict(zip(selected, shares))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        friends_input = request.form.get('friends', '')
        bill_amount_input = request.form.get('bill_amount', '0')
        mode = request.form.get('mode')  # now reads from form
        split_mode = mode == 'split'
        split_count_input = request.form.get('split_count', '').strip()

        friends = [f.strip() for f in friends_input.split(',') if f.strip()]
        total_friends = len(friends)

        try:
            bill_amount = float(bill_amount_input)
            if bill_amount <= 0:
                raise ValueError
        except ValueError:
            return render_template('index.html', error="Enter a valid positive bill amount.",
                                   friends=friends_input, bill_amount=bill_amount_input, split_mode=split_mode)

        if not friends:
            return render_template('index.html', error="Please enter at least one friend's name.",
                                   friends=friends_input, bill_amount=bill_amount_input, split_mode=split_mode)

        if split_mode:
            try:
                split_count = int(split_count_input)
                if split_count < 1 or split_count > total_friends:
                    raise ValueError
            except ValueError:
                return render_template('index.html', error="Enter a valid number of people to split the bill.",
                                       friends=friends_input, bill_amount=bill_amount_input, split_mode=split_mode)

            split_result = random_split(bill_amount, friends, split_count)
            return render_template('index.html', split_mode=True, split_result=split_result,
                                   bill_amount=int(bill_amount), friends=friends_input)
        else:
            payer = random.choice(friends)
            return render_template('index.html', split_mode=False, payer=payer,
                                   bill_amount=int(bill_amount), friends=friends_input)

    return render_template('index.html')
