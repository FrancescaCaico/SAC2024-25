import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

//  DELAY --> IN[], OUT 
//  SOURCE --> OUT
//  SINK --> IN[]
//  QUEUE --> IN[] , OUT
//  ROUTER --> IN[] , OUT []


network lognormal {
    parameters:
        double mu = default(100); 
        double rho =  default(0.7);  // UTILIZZAZIONE 
        double lambda = default(rho*mu);
        double cv = default(0.5);
        src.interArrivalTime = 1s * exponential(1/lambda); 
        srv.serviceTime =1s * lognormal(log(1.0/(mu*sqrt(1+cv^2))), sqrt(log(1+cv^2)));
        srv.capacity = -1;

    submodules:
        src: Source; 
        srv: Queue; 
        sink : Sink;
    connections:
        src.out --> srv.in++; 
        srv.out --> sink.in++;
  
        
}





// #rho	cv	ResponseTime	        sigma(ResponseTime)	    QueueTime	            sigma(QueueTime)
// 0.7	0.5	0.024813709516635002	0.0005719166551057231	0.014826492539371334	0.0005554568772409807
// 0.7	1.0	0.033239530040971334	0.0008203236739303503	0.023251228819442332	0.0008033106341884599
// 0.7	1.5	0.048522819455707994	0.0022271152069378965	0.03850126696363033	    0.0021881943971557155
// 0.9	0.5	0.06731000724869567	    0.0053177889419716165	0.057318527794714	    0.00531046971077656
// 0.9	1.0	0.11606968136872532	    0.01644113387894572	    0.10603731628822366	    0.016376308503812623
// 0.9	1.5	0.16749960004361666	    0.038012235208977375	0.15751043485227	    0.03798365047852918

// intervalli di confidenza 

// #rho	cv	ResponseTime	+-        sigma(ResponseTime)	    QueueTime	            sigma(QueueTime)
// 0.7	0.5	(0.024813709516635002 +- 0.0005719166551057231)	0.014826492539371334 +- 0.0005554568772409807
// 0.7	1.0	(0.033239530040971334 +- 0.0008203236739303503)	0.023251228819442332 +-	0.0008033106341884599
// 0.7	1.5	(0.048522819455707994 +- 0.0022271152069378965)	0.03850126696363033	 +- 0.0021881943971557155
// 0.9	0.5	(0.06731000724869567 +-  0.0053177889419716165)	0.057318527794714	 +- 0.00531046971077656
// 0.9	1.0	0.11606968136872532	 +-  0.01644113387894572	0.10603731628822366	 +- 0.016376308503812623
// 0.9	1.5	0.16749960004361666	 +-  0.038012235208977375	0.15751043485227	 +- 0.03798365047852918