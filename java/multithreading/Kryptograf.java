import java.util.concurrent.CountDownLatch;

/**
 * Kryptografklasse. Henter ut meldinger, dekrypterer og sender videre.
 */
class Kryptograf implements Runnable {

    Monitor utMonitor;
    Monitor innMonitor;
    Melding melding;
    String dekryptertMelding;
    String navn;

    /**
     * Henter meldinger fra innMonitor, dekrypterer de, og sender de
     * til utMonitor. Avslutter når det er tomt.
     *
     * @param ID    Personlig ID-nummer
     */
    Kryptograf(int ID, Monitor innMonitor, Monitor utMonitor) {
	this.navn       = ( "Kryptograf nr." + ID );
	this.innMonitor = innMonitor;
	this.utMonitor  = utMonitor;
    }

    public void run() {

	while (true) {
	    melding = innMonitor.hentUt(navn);
	    if (melding == null) { // Ingen flere meldinger å hente
		utMonitor.settInn(melding, navn); // Signaliserer monitor
		break;
	    }
	    dekryptertMelding = Kryptografi.dekrypter(melding.hentMelding());
	    melding.endreMelding(dekryptertMelding);
	    utMonitor.settInn(melding, navn);
	}
    }
}
