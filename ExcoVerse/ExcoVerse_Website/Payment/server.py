# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import stripe
stripe.api_key = "sk_test_51NPQo0HLT8WmDutBFqvUGugxoLESvZLHVse03ccDBJhV4sCCor47wDlK128kVi0OTsK9rhYrPhH7rF7wnFNLJliS00di72Mrdz"

stripe.Account.create(
  type="custom",
  country="SG",
  capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}},
)