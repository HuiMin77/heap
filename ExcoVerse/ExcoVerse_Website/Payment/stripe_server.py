# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import stripe
stripe.api_key = "pk_live_51NPQo0HLT8WmDutBjgcMGG5YLyJkRBLOB16RpVvceJ1LJ43llooXY1hlF4ey0SekNF0UrMFJo1dJQoefh0LIo2UT00uvMPt0Ud"

def create_connected_account():
    account = stripe.Account.create(
        type="standard",  # Use "standard" or another account type as needed
        country="US",  # Replace with the country code of the connected account
        email="viciky023@gmail.com",  # Replace with the email of the connected account
    )
    return account



stripe.AccountLink.create(
  account=CONNECTED_ACCOUNT_ID,
  refresh_url="https://example.com/reauth",
  return_url="https://example.com/return",
  type="account_onboarding",
)

stripe.checkout.Session.create(
  mode="payment",
  line_items=[{"price": '{{PRICE_ID}}', "quantity": 1}],
  payment_intent_data={"application_fee_amount": 123},
  success_url="https://127.0.0.1:8000/checkout.html",
  cancel_url="https://example.com/cancel",
  stripe_account='{{CONNECTED_ACCOUNT_ID}}',
)