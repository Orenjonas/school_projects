import java.io.*;
import java.util.ArrayList;

/** 
 * A Program that simulates telegraphists sending messages to an operations central (Monitor)
 * where cryptographers collect and decrypt the messages and pass them on to a new cenral
 *
 * The code is in norwegian, as this was the course language.
 */


class Hovedprogram {

    static int antTelegrafister = 3;
    static int antKryptografer  = 30;
    static Operasjonssentral sentral = new Operasjonssentral(antTelegrafister);
    static Kanal[] kanaler           = sentral.hentKanalArray();

    static Monitor  kryptertMonitor = new Monitor(antTelegrafister);
    static Monitor ukryptertMonitor = new Monitor(antKryptografer);


    public static void main(String[] args) {

	// Start all the actors (threads), the creation of threads are also separate threads
	new Thread(new LagOgSettIGangTelegrafister()).start();
	new Thread(new LagOgSettIGangKryptografer()).start();
	new Thread(new Operasjonsleder(ukryptertMonitor)).start();
    }

    static class LagOgSettIGangTelegrafister implements Runnable {
	/** 
	 * Create and start telegraphist threads
	 */
	public void run() {
	    Telegrafist telegrafist;
	    for (int i = 0 ; i < antTelegrafister ; i ++) {
		System.out.println("Setter i gang telegrafist nr." + (i+1) );
		telegrafist = new Telegrafist(i, kanaler[i], kryptertMonitor);
		new Thread(telegrafist).start();
	    }
	}
    }
    static class LagOgSettIGangKryptografer implements Runnable {
	/** 
	 * Create and start cryptographer threads
	 */
	public void run() {
	    Kryptograf kryptograf;
	    for (int i = 0 ; i < antKryptografer ; i++ ) {
		System.out.println("Setter i gang kryptograf nr." + (i+1));
		kryptograf = new Kryptograf(i, kryptertMonitor, ukryptertMonitor);
		new Thread(kryptograf).start();
	    }
	}
    }
}
