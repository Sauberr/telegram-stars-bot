hello-msg =
    <b>👊 Hello!</b>
    If you decided to support the author with a donation, then use the following commands:

    • /donate [amount]: donate the specified number of stars (example. /donate 100)
    • /paysupport: help with purchases
    • /refund: refund the donation if no more than 14 days have passed

donate-invoice-title =
    Donate to the author

donate-invoice-description =
    For the amount of {$amount ->
        [one] {$amount} star
        [few] {$amount} stars
       *[other] {$amount} stars
    }

donate-button-pay =
    Pay {$amount} XTR

donate-button-cancel =
    Cancel the operation

donate-input-error =
    Please enter the amount in the format <code>/donate [NUMBER]</code>, where [NUMBER] is the donation amount, from ⭐️ 1 to ⭐️ 2500.

    Examples:
    • <code>/donate 100</code> - donate 100 ⭐️
    • <code>/donate 500</code> - donate 500 ⭐️
    • <code>/donate 1000</code> - donate 1000 ⭐️

donate-paysupport-tid-tip =
    <blockquote>You can get it after you pay for the donation.
    Just click on the message <b>"You have successfully transferred ⭐️ .."</b> and copy the transaction ID from there.</blockquote>

donate-paysupport-message =
    If you want to issue a refund, use the /refund command

    🤓 You will need a transaction ID.
    {donate-paysupport-tid-tip}

donate-refund-input-error =
    Please provide the transaction ID in the format <code>/refund [id]</code>, where [id] is the transaction ID you received after donating.

    {donate-paysupport-tid-tip}

donate-refund-success =
    Refund was successful. The stars spent have already been returned to your Telegram account.

donate-refund-code-not-found =
    Transaction with the specified identifier not found. Please check the entered data and try again.

donate-refund-already-refunded =
    A refund for this transaction has already been made.

# no html etc. (msg for callback answer)
donate-cancel-payment =
    😢 Donation canceled.

donate-successful-payment =
    <b>🫡 Thank you!</b>
    Your donation has been successfully accepted.







hello-owner =
    <b>👊 Hello, owner!</b>

ping-msg =
    <b>👊 Up & Running!</b>

media-msg =
    <b>🫡 Nice media <i>(I guess)</i>!</b>