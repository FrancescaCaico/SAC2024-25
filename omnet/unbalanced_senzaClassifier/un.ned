import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

//  DELAY --> IN[], OUT 
//  SOURCE --> OUT
//  SINK --> IN[]
//  QUEUE --> IN[] , OUT
//  ROUTER --> IN[] , OUT []

// La rete ha due generatori di carico:
//  • LowLoadSrc che invia richieste con un tasso λ −δ
//  • HiLoadSrc che invia richieste con un tasso λ + δ
// Con λ = 6 richieste al secondo
// Entrambi i server hanno un processing rate μ = 10 richieste al secondo. Si chiede
// di mostrare il tempo di risposta Tr,  l’utilizzazione dei server ρ per diversi valori
// di δ (espresso in richieste al secondo):

network un {
    parameters:
        double lambda =  default(6.0); 
        double mu = default(10.0); 
        double sigma = default(0.0); 
        LowLoadSrc.interArrivalTime = 1s * exponential(1/(lambda-sigma)); 
        HiLoadSrc.interArrivalTime = 1s * exponential(1/(lambda+sigma)); 
        
        LowLoadSrv.serviceTime= 1s * exponential(1/mu); 
        HiLoadSrv.serviceTime= 1s * exponential(1/mu); 

        LowLoadSrv.capacity=-1; 
        HiLoadSrv.capacity=-1; 

    submodules:
        LowLoadSrc : Source; 
        HiLoadSrc : Source; 

        LowLoadSrv : Queue;
        HiLoadSrv : Queue;
        
        Sink : Sink; 
    connections:
        LowLoadSrc.out --> LowLoadSrv.in++; 
        LowLoadSrv.out --> Sink.in++;
        HiLoadSrc.out --> HiLoadSrv.in++; 
        HiLoadSrv.out --> Sink.in++;  
        
}

// PRIMO PUNTO --> RISULTATI
// #sigma	ResponseTimeMean	sigma(ResponseTimeMean)	ResponseTimeMax	    sigma(ResponseTimeMax)	UtilizationHi	    sigma(UtilizationHi)	UtilizationLow	    sigma(UtilizationLow)
// 0.0	    0.250821344844528	0.0016346851653588946	2.8215078764455996	0.3956077951870905	    0.599963183548438	0.0029900875227670816	0.60046554629686	0.004875149301348858
// 1.0	    0.276659826423184	0.006955990307179615	3.0367808516354002	0.4017982013755957	    0.700296380239786	0.005517194287309255	0.49936850751324197	0.00269461345059101
// 2.0	    0.39467646623839997	0.009026333733373172	4.613085638878999	0.6201615424042662	    0.8021576187135301	0.0025179626129563978	0.399797876467058	0.0025282357787534885
// 3.0  	0.793385074466294	0.0345739254364186	    7.206295138141199	0.7184446410821842	    0.90157261448865	0.00385747023431472	    0.2995929911705161	0.001116007761013667
