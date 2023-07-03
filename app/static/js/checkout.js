const form = document.querySelector('#payment-form');

form.addEventListener('submit', handleSubmit);

let elements;
let emailAddress = '';

async function initialize(url) {
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': form.elements[name='csrfmiddlewaretoken'].value,
        },
        credentials: 'same-origin',
    });
    const { clientSecret } = await res.json();

    const appearance = {
        theme: 'stripe',
    };

    elements = stripe.elements({ appearance, clientSecret });

    const linkAuthenticationElement = elements.create('linkAuthentication');
    linkAuthenticationElement.mount('#link-authentication-element');

    linkAuthenticationElement.on('change', (event) => {
        emailAddress = event.value.email;
    });

    const paymentElementOptions = {
        layout: 'tabs',
    };

    const paymentElement = elements.create('payment', paymentElementOptions);
    paymentElement.mount('#payment-element');
}

async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: 'http://localhost:8000/cart/success/',
            receipt_email: emailAddress,
        },
    });

    if (error.type === 'card_error' || error.type === 'validation_error') {
        alert(error.message);
    } else {
        alert('An unexpected error occurred.');
    }

    setLoading(false);
}

async function checkStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
        'payment_intent_client_secret'
    );

    if (!clientSecret) {
        return;
    }

    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

    switch (paymentIntent.status) {
        case "succeeded":
            alert("Payment succeeded!");
            break;
        case "processing":
            alert("Your payment is processing.");
            break;
        case "requires_payment_method":
            alert("Your payment was not successful, please try again.");
            break;
        default:
            alert("Something went wrong");
            break;
    }
}

function setLoading(isLoading) {
    if (isLoading) {
        document.querySelector('#submit').disabled = true;
        document.querySelector('#spinner').classList.remove('d-none');
        document.querySelector('#button-text').classList.add('d-none');
    } else {
        document.querySelector('#submit').disabled = false;
        document.querySelector('#spinner').classList.add('d-none');
        document.querySelector('#button-text').classList.remove('d-none');
    }
}
