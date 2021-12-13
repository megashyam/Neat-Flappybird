# Neat-Flappybird

Implemented the classic Flappybird game with AI using the NEAT module.The bird evolves every generation with the children being the last surviving bird of the previous generation. 



![image](https://user-images.githubusercontent.com/67580678/145761327-7193107e-7955-400d-9c1f-7840454ac14e.png)



#### What is NEAT?

NEAT (NeuroEvolution of Augmenting Topologies) is an evolutionary algorithm that creates artificial neural networks.
Each genome contains two sets of genes that describe how to build an artificial neural network:

  1. Node genes, each of which specifies a single neuron.
  2. Connection genes, each of which specifies a single connection between neurons.


The user must provide a fitness function which computes a single real number indicating the quality of an individual genome: better ability to solve the problem means a higher score. The algorithm progresses through a user-specified number of generations, with each generation being produced by reproduction and mutation of the most fit individuals of the previous generation.

The reproduction and mutation operations may add nodes and/or connections to genomes, so as the algorithm proceeds genomes may become more and more complex. When the preset number of generations is reached, or when at least one individual  exceeds the user-specified fitness threshold, the algorithm terminates.

## Encoding

The NEAT algorithm chooses a direct encoding methodology. It has two lists of genes, a series of nodes and a series of connections.


![image](https://user-images.githubusercontent.com/67580678/145758700-fadbaad8-c065-47e9-9635-7d8399476d73.png)

## Mutation
In NEAT, mutation can either mutate existing connections or can add new structure to a network. If a new connection is added between a start and end node, it is randomly assigned a weight.
If a new node is added, it is placed between two nodes that are already connected. The previous connection is disabled. The previous start node is linked to the new node with the weight of the old connection and the new node is linked to the previous end node with a weight of 1. This was found to help mitigate issues with new structural additions.


![image](https://user-images.githubusercontent.com/67580678/145758766-3a4fdac0-b6bc-42c7-bbe5-e3d98905b6b5.png)

## Competing Conventions

The idea is that just blindly crossing over the genomes of two neural networks could result in networks that are horribly mutated and non-functional. If two networks are dependent on central nodes that both get recombined out of the network, there arises an issue.

How do we align genomes that don’t seem to be obviously compatible? In biology, this is taken care of through an idea called homology. Homology is the alignment of chromosomes based on matching genes for a specific trait. Once that happens, crossover can happen with much less chance of error than if chromosomes were blindly mixed together.
NEAT tackles this issue through the usage of historical markings (as seen above). By marking new evolutions with a historical number, when it comes time to crossover two individuals, this can be done with much less chance of creating individuals that are non-functional. Each gene can be aligned and crossed-over. Each time a new node or new type of connection occurs, a historical marking is assigned, allowing easy alignment when it comes to breed two individuals.


![image](https://user-images.githubusercontent.com/67580678/145757281-c4335fe9-ec32-40eb-bb07-861cd0fe0a0a.png)


## Speciation

Adding a new connection or node before any optimization of weights have occurred often leads to a lower performing individual. This puts new structures at a disadvantage. How can we protect new structures and allow them to optimize before we eliminate them from the population entirely? NEAT suggests speciation.
Speciation simply splits up the population into several species based on the similarity of topology and connections. Individuals in a population only have to compete with other individuals within that species. This allows for new structure to be created and optimized without fear that it will be eliminated before it can be truly explored.




