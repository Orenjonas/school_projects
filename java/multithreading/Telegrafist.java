import java.util.concurrent.CountDownLatch;

class Telegrafist implements Runnable {

    private String navn; // Brukes til rapportering under kjøring
    private Kanal kanal;
    private int kanalID;
    private Monitor utMonitor;
    private String tekst;
    private Melding melding;


    /** Motta tekst og lag meldinger som sendes
     * til utMonitor
     */
    Telegrafist(int ID, Kanal k, Monitor utMonitor) {
	this.navn = ( "Telegrafist nr." + ID );
	this.kanal = k;
	this.kanalID = k.hentId();
	this.utMonitor = utMonitor;
    }

    public void run() {
	do {
	    tekst = kanal.lytt();
	    if (tekst == null) { melding = null;}
	    else               { melding = new Melding(tekst, kanalID);}
	    utMonitor.settInn(melding, navn);
	} while(tekst != null);
    }
}

