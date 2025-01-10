import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Classifier;

//  DELAY --> IN[], OUT 
//  SOURCE --> OUT
//  SINK --> IN[]
//  QUEUE --> IN[] , OUT
//  ROUTER --> IN[] , OUT []

// Valutare la possibilità di prendere i dati relativi alle due sorgenti dati. Per farlo:
//  • Studiare l’uso della proprietà jobType nel componente Source
//  • Studiare il componente Classifier con particolare riferimento alla proprietà dispatcherField
//  • Modificare la rete per aver due Sink e un Classifier che smista il traffico tra i due
//  • Ri-valutare i tempi di risposta medi dei due server nei due problemi precedenti

network un3 {
    parameters:
        double lambda =  default(6.0); 
        double mu = default(10.0); 
        double sigma = default(0.0); 
        LowLoadSrc.interArrivalTime = 1s * exponential(1/(lambda)); 
        HiLoadSrc.interArrivalTime = 1s * exponential(1/(lambda)); 

        LowLoadSrc.jobType = default(0); 
        HiLoadSrc.jobType = default(1); 
        
        LowLoadSrv.serviceTime= 1s * exponential(1/(mu+sigma)); 
        HiLoadSrv.serviceTime= 1s * exponential(1/(mu-sigma)); 

        LowLoadSrv.capacity=-1; 
        HiLoadSrv.capacity=-1; 

        Classifier.dispatchField = "type";

    submodules:
        LowLoadSrc : Source; 
        HiLoadSrc : Source; 

        LowLoadSrv : Queue;
        HiLoadSrv : Queue;
        
        Sink1 : Sink; 
        Sink2 : Sink; 
        Classifier: Classifier {
            gates:
                in[2];
                out[2];
        }; 
    connections:
        LowLoadSrc.out --> LowLoadSrv.in++; 
        LowLoadSrv.out --> Classifier.in[0];
        Classifier.out[0] --> Sink1.in++; 
        HiLoadSrc.out --> HiLoadSrv.in++; 
        HiLoadSrv.out --> Classifier.in[1]; 
        Classifier.out[1] --> Sink2.in++; 
        Classifier.rest --> Sink1.in++;
        
}

