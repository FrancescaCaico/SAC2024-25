import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source; 
import org.omnetpp.queueing.Delay; 

//  DELAY --> IN[], OUT 
//  SOURCE --> OUT
//  SINK --> IN[]
//  QUEUE --> IN[] , OUT

// Identificare il tempo di risposta complessivo Tr nel caso in cui fl = 0.7. 
// Indicare anche l’intervallo di confidenza del 67% per tali valori [ Valore atteso: 0.296 sec] 


network simulazione3{
    parameters: 
        double lambda = default(10); 
        double mu = default(10);
        double ft = default(0.7);

        double lambda_l = lambda * ft ;
        double lambda_c = lambda*(1-ft);

        LocalSrc.interArrivalTime = 1s * exponential(1/lambda_l);
        LocalProcessing.serviceTime = 1s * exponential(1/mu);
        
        CloudSrc.interArrivalTime = 1s * exponential(1/lambda_c);

        double d = default(0.1);
        CloudDelay.delay = 1s * truncnormal(1/mu, 0.1*d);
        CloudProcessing.delay = 1s * truncnormal(1/mu, 0.1*d);
        LocalProcessing.capacity = -1;

    submodules:
        LocalSrc: Source;
        CloudSrc: Source;

        LocalProcessing: Queue;
        CloudProcessing: Delay;
        CloudDelay: Delay;

        sink : Sink;

    connections:
        LocalSrc.out --> LocalProcessing.in++; 
        LocalProcessing.out -->  sink.in++; 
        
        CloudSrc.out --> CloudDelay.in++; 
        CloudDelay.out --> CloudProcessing.in++;
        CloudProcessing.out --> sink.in++;
}