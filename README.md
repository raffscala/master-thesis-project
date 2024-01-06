# Master Thesis in Computational Astrophysics
Here I present the codes I realized for my master thesis in Computational Astrophisics. In this work, through computational methods, I studied the occurrences and the characteristics of peculiar supernova types: the pair insatibility and pulastional pair instability supernova. From the scientific point of view, these events are very interesting because we have never observed them with our telescopes and, furthermore, they originate from extremely massive stars (more than a hundred solar masses).

During my work I carried out several simulations regarding the evolution in time of stellar populations. In order to do this, I adopted the C++ population synthesis code SEVN [(Iorio et al., 2023)](https://ui.adsabs.harvard.edu/abs/2023MNRAS.524..426I/abstract). As results of the simulations I obtained a **large amount of data** (~1TB) which I processed and analysed developing the Python codes stored in the folder [SEVN_data_analysis](https://github.com/raffscala/master-thesis-project/tree/main/SEVN_data_analysis)
Furthermore, I updated the Python code Cosmorate [(Santoliquido et al., 2021)](https://ui.adsabs.harvard.edu/abs/2021MNRAS.502.4877S/abstract), that was meant for a different aim, to evaluate the occurrences of the supernovae during the Universe history. In order to make use of Cosmorate I needed to generate proper input files starting from the output of the aforemantioned simulations. The codes I developed for this purpose are stored in the folder [cosmorate_initial_conditions](https://github.com/raffscala/master-thesis-project/tree/main/cosmorate_initial_conditions). 
Lastly in the folder [plot](https://github.com/raffscala/master-thesis-project/tree/main/plot) I reported the plots representing my results and the scripts I wrote to creat them.
