/**
* Name: NetworkTest
* Based on the internal empty template. 
* Author: Lili
* Tags: 
*/


model NetworkTest


global {
	int simulation_id<-0;
	
	string prefix_client <- "Client_";
	
	init {
		
		create TCP_Client number:5 {
			simulation_id <-simulation_id+1;
			name <- prefix_client+string(simulation_id);
			// replace the "localhost" address by the IP address of the other computer 
			do connect to: "localhost" protocol: "tcp_client" port: 9999 with_name: "Client";
		}
		
		create UDP_Server number:1{
			do connect to: "localhost" protocol: "udp_server" port: 9877 ;
		}
		
	}

}


// Client that request throught TCP protocol
species TCP_Client skills: [network] {

	string name;
	reflex receive when:has_more_message() {
		loop while:has_more_message() {
			message mm <- fetch_message();
			//write mm.contents;
		}
	}



	reflex send when:every(100#cycle) { 
		string mm <- "Hola mi nombre es: "+name;
		do send  contents: mm;
	}
		
}


species UDP_Server skills: [network]
{
	reflex fetch when:has_more_message() {	
		loop while:has_more_message()
		{
			message s <- fetch_message();
			list coordinates <- string(s.contents) split_with(";");
			write s;
		}
	}
	
}


experiment "Request_Response" type: gui
{
	output
	{
	}
}

