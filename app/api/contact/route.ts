import { NextRequest, NextResponse } from 'next/server';
import { Resend } from 'resend';

export async function POST(request: NextRequest) {
  try {
    // Verifica che le variabili d'ambiente siano presenti
    if (!process.env.RESEND_API_KEY) {
      console.error('RESEND_API_KEY non configurata');
      return NextResponse.json(
        { error: 'Configurazione server mancante' },
        { status: 500 }
      );
    }

    if (!process.env.RESEND_EMAIL) {
      console.error('RESEND_EMAIL non configurata');
      return NextResponse.json(
        { error: 'Configurazione server mancante' },
        { status: 500 }
      );
    }

    const resend = new Resend(process.env.RESEND_API_KEY);
    const { name, email, message } = await request.json();

    // Validazione base
    if (!name || !email || !message) {
      return NextResponse.json(
        { error: 'Tutti i campi sono obbligatori' },
        { status: 400 }
      );
    }

    // Invio email tramite Resend
    const { data, error } = await resend.emails.send({
      from: 'onboarding@resend.dev',
      to: process.env.RESEND_EMAIL,
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

    if (error) {
      console.error('Errore Resend:', error);
      return NextResponse.json(
        { error: 'Errore durante l\'invio del messaggio', details: error },
        { status: 500 }
      );
    }

    console.log('Email inviata con successo:', data);
    return NextResponse.json(
      { success: true, message: 'Messaggio inviato con successo!' },
      { status: 200 }
    );
  } catch (error) {
    console.error('Errore invio email:', error);
    return NextResponse.json(
      { error: 'Errore durante l\'invio del messaggio', details: String(error) },
      { status: 500 }
    );
  }
}
