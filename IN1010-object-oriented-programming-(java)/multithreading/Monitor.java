import java.util.concurrent.locks.*;
import java.util.concurrent.*;
import java.util.LinkedList;
import java.util.concurrent.CountDownLatch;

/** 
 * Holder styr på meldinger, og signaliserer til trådene.
 */
class Monitor {

    private Lock laas                     = new ReentrantLock();
    private Condition ikkeTom             = laas.newCondition();
    private Condition sluttPaaInnsending  = laas.newCondition();
    private LinkedList<Melding> meldinger = new LinkedList<>();

    private int aktiveInnsendere;


    Monitor(int antInnsendere) {
	this.aktiveInnsendere = antInnsendere;
    }

    public void settInn(Melding innMelding, String navn) {
	laas.lock();
	try {
	    if (innMelding == null) {
		aktiveInnsendere --;
		if (aktiveInnsendere == 0) {  // Tomt for meldinger og ingen flere pa vei.
		    System.out.println("\n" + navn + ": **** Alle innsendere ferdig ****\n");
		    ikkeTom.signalAll();
		    sluttPaaInnsending.signal();
		}
	    } else {
		meldinger.add(innMelding);
		System.out.println( navn + ": melding nr."+innMelding.hentSekvensnummer()+" sendt inn");
		ikkeTom.signal();
	    }
	} finally {
	    laas.unlock();
	}
    }

    public Melding hentUt(String navn) {

	laas.lock();

	try{
	    while (meldinger.isEmpty()) { // Test om tomt (også etter ikkeTom.signal())
		if (aktiveInnsendere == 0) { // Innsendere ferdig, rett til finally blokk 
		    return null;
		} else {
		    // Venting
		    try {
			System.out.println( navn + ": Venter pa meldinger");
			ikkeTom.await();
		    } catch (InterruptedException ex) {
			System.out.println( navn + "Uventet avbrudd");
		    }
		}
	    }
	    System.out.println( navn + ": Henter ut melding");
	    return meldinger.pop();
	} finally {
	    laas.unlock();
	}
    }


    /** 
     * Operasjonslederen venter til alle er ferdig og henter så ut
     * meldingene
     * @return    ferdig dekrypterte meldinger
     */
    public LinkedList<Melding> hentMeldinger() {

	laas.lock();
	try {
	    if (aktiveInnsendere != 0) {
		try {
		    System.out.println("Operasjonsleder venter på meldinger");
		    sluttPaaInnsending.await();
		} catch (InterruptedException ex) {
		    System.out.println("Uventet avbrudd under venting på uthenting av meldinger-liste: " + ex);
		}
	    }
	    return meldinger;
	} finally {
	    laas.unlock();
	}
    }
}
