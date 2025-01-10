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

network un2 {
    parameters:
        double lambda =  default(6.0); 
        double mu = default(10.0); 
        double sigma = default(0.0); 
        LowLoadSrc.interArrivalTime = 1s * exponential(1/(lambda)); 
        HiLoadSrc.interArrivalTime = 1s * exponential(1/(lambda)); 
        
        LowLoadSrv.serviceTime= 1s * exponential(1/(mu+sigma)); 
        HiLoadSrv.serviceTime= 1s * exponential(1/(mu-sigma)); 

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

// #sigma	ResponseTimeMean	sigma(ResponseTimeMean)	ResponseTimeMax	    sigma(ResponseTimeMax)	UtilizationHi	sigma(UtilizationHi)	    UtilizationLow	    sigma(UtilizationLow)
// 0.0	    0.250821344844528	0.0016346851653588946	2.8215078764455996	0.3956077951870905	    0.599963183548438	0.0029900875227670816	0.60046554629686	0.004875149301348858
// 1.0	    0.26417718708067406	0.0072650643897265435	3.3988674167206	    0.43260479470302643	    0.66465113550343	0.003959142485332724	0.5446182672805799	0.00102443739291378
// 2.0	    0.33340150730193796	0.005842511567483036	4.2400010433342	    0.7237083386870373	    0.74987418707854	0.00521816813259418	    0.500189182205474	0.0010820226151564995
// 3.0	    0.5852202410896861	0.02682332642982855	    8.0796234568584	    0.6688498832318068	0.858249503861158	0.0030929141388975514	    0.46047019396484	0.0009538025455630644
