This is a fresh project. The goal is to check a hypothesis about the interface of cultural and genetic evolution. We assume a population of individuals that can interact with each other, leaving it open what precisely this means. The number of interactions an individual makes is a primitive. The propensity to interactions is determined by your genes and your memes. Everyone carries, say 100 1 bit memes and 100 1 bit genes. If all are 0 you do roughly 0 interactions per turn, if all are 1 you do 200.

  There is a genetic replicator dynmaic going on. Stipulate a fitness function such that 30 interactions are biologically optimal.

  But there is also memetic replicator dynmaic going on: You memes can randomly catch 1 meme of someone else at each interaction. This is how memes that push for interaction replicate more. Let this be 10 times faster than the genetic replicator dynmaic, having 1 genetic update per 10 memtic ones.

  Let this run for a while. Start with a random distribution of genes and only a few memes being turned to cooperation.

  Make one png with four plots. Top row: just biological evolution, bottom row with memetic evolution turned on. Left column the mean number of interactions per turn. Right column the genetically and memetically prefered number of interactions per turn.

  Set up uv. Write this into the readme cleanly without adding things in the theory section. Put additions from your side in the implementation section.