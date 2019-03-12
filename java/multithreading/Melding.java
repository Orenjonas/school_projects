/** 
 * Denne filen er skrevet av fagansvarlig.
 */

class Melding implements Comparable<Melding> {

    private static int IDTeller;
    private int kanalID;
    private int sekvensnummer;
    private String melding;
    
    Melding(String m, int kID) {
	this.melding = m;
	this.kanalID = kID;
	// burde ID oppdateres i monitor med lock?
	this.sekvensnummer = IDTeller;
	IDTeller ++;
    }

    public int hentSekvensnummer() {
	return sekvensnummer;
    }

    public int hentKanalID() {
	return kanalID;
    }

    public void endreMelding(String m) {
	this.melding = m;
    }

    public String hentMelding(){
	return melding;
    }

    @Override
    public int compareTo(Melding m) {
	if (kanalID > m.hentKanalID()) return 2;
	if (kanalID < m.hentKanalID()) return -2;
	if (sekvensnummer > m.hentSekvensnummer()) return 1;
	if (sekvensnummer < m.hentSekvensnummer()) return -1;
	else return 0;
    }
}
