import { NextRequest, NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: NextRequest) {
  try {
    const { name, email, message } = await request.json();

    // Validazione base
    if (!name || !email || !message) {
      return NextResponse.json(
        { error: 'Tutti i campi sono obbligatori' },
        { status: 400 }
      );
    }

    // Invio email tramite Resend
    await resend.emails.send({
      from: 'onboarding@resend.dev',
      to: process.env.RESEND_EMAIL!,
      replyTo: email,
      subject: `Nuovo messaggio da ${name}`,
      html: `
        <h1>Nuovo messaggio dal form di contatto</h1>
        <p><strong>Nome:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Messaggio:</strong></p>
        <p>${message.replace(/\n/g, '<br>')}</p>
      `,
    });

    return NextResponse.json(
      { success: true, message: 'Messaggio inviato con successo!' },
      { status: 200 }
    );
  } catch (error) {
    console.error('Errore invio email:', error);
    return NextResponse.json(
      { error: 'Errore durante l\'invio del messaggio' },
      { status: 500 }
    );
  }
}
