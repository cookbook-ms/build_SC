

from SimplicialComplex.SimplicialComplex import SimplicialComplex

if __name__ == "__main__":
    file_name = 'email-Enron'
    list_simplices = SimplicialComplex(file_name, top_dim=4, percentage_time=1)
