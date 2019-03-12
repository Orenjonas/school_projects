import java.util.LinkedList;
import java.util.Collections;
import java.io.*;

/**
 * Henter ut dekrypterte meldinger og sorterer de
 * i rett rekkefølge etter kanalID
 */
class Operasjonsleder implements Runnable {

    Monitor innMonitor;
    LinkedList<Melding>             meldinger;


    Operasjonsleder(Monitor innMonitor) {
	this.innMonitor = innMonitor;
    }

    @Override
    public void run() {
	meldinger = innMonitor.hentMeldinger(); // Henter dekrypterte meldinger

	Collections.sort(meldinger); // Sorter dem

	String tekster = "";
	int forrigeKanal = meldinger.get(0).hentKanalID();
	int denneKanalen;

	for (Melding m : meldinger) { // Loop over meldingene og skriv til en til.
	    denneKanalen = m.hentKanalID();
	    if (denneKanalen > forrigeKanal) { // Legg til paragraf ("\n\n") når meldingen stammer fra en annen kanal
		forrigeKanal = denneKanalen;
		tekster += "\n\n";
	    }
	    tekster += m.hentMelding() + "\n";
	}

	System.out.println("Operasjonsleder: meldinger skrives til fil \"Tekster.txt\"");
	try {
	    PrintWriter skriver = new PrintWriter("Tekster.txt", "UTF-8");
	    skriver.print(tekster);
	    skriver.close();
	} catch (FileNotFoundException ex) {
	    System.out.println("Feil ved skriving av fil: " + ex);
	} catch (UnsupportedEncodingException ex) {
	    System.out.println("Feil skriving av fil: " + ex);
	}
	System.out.println("Operasjonsleder: fil \"Tekster.txt\" skrevet");
    }
}
