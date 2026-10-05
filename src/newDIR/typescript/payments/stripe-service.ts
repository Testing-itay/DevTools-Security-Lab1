import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? '');

export async function createPaymentIntent(
  amount: number,
  currency: string,
  metadata?: Record<string, string>
): Promise<Stripe.PaymentIntent> {
  return stripe.paymentIntents.create({
    amount,
    currency,
    metadata,
    automatic_payment_methods: { enabled: true },
  });
}

export async function createCustomer(
  email: string,
  name?: string
): Promise<Stripe.Customer> {
  return stripe.customers.create({ email, name });
}
