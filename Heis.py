import numpy as np
from numpy import linalg as la

#Pauli matrices
x = np.array([[0,1],[1,0]])
y = np.array([[0, -1j], [1j,0]])
z = np.array([[1,0], [0,-1]])

#Spin up and down
Up = np.array([[1],[0]])
Down = np.array([[0], [1]])

#Spin operators
sx = 1./2*x
sy = 1./2*y
sz = 1./2*z

splus = np.array([[0,1],[0,0]])
sminus = np.array([[0,0],[1,0]])
I = np.identity(2)

#Defining basis of all possible combinations of spins for n particles
def particleInit(particles): # not necessary
    for i in range(0,1<<particles):
	B = np.arange(1<<particles)
	B = B.reshape((1<<particles,1))
	C = np.zeros_like(B)
	C_i = C
	C_i[1-i,0] = 1
	#print(C_i)

particleInit(3)

#Spin operators
#Sz Operator
def spinoperatorz(particles,index): 
    if particles == index: 
        P_i = sz
    else:
        P_i = I
    for i in range(1, particles): 
        if (particles-i) == index: 
            P_i = np.bmat([[sz[0,0]*P_i, sz[0,1]*P_i], [sz[1,0]*P_i, sz[1,1]*P_i]]) 
        else:
            P_i = np.bmat([[I[0,0]*P_i, I[0,1]*P_i], [I[1,0]*P_i, I[1,1]*P_i]]) 
    return(P_i) 
  
#Splus operator
def spinoperatorplus(particles,index): 
    if particles == index: 
        P_i = splus
    else:
        P_i = I
    for i in range(1, particles): 
        if (particles-i) == index:  
            P_i = np.bmat([[splus[0,0]*P_i, splus[0,1]*P_i], [splus[1,0]*P_i, splus[1,1]*P_i]]) 
        else:
            P_i = np.bmat([[I[0,0]*P_i, I[0,1]*P_i], [I[1,0]*P_i, I[1,1]*P_i]]) 
    return(P_i) 

#Sminus operator
def spinoperatorminus(particles,index): 
    if particles == index: 
        P_i = sminus
    else:
        P_i = I
    for i in range(1, particles): 
        if (particles-i) == index:  
            P_i = np.bmat([[sminus[0,0]*P_i, sminus[0,1]*P_i], [sminus[1,0]*P_i, sminus[1,1]*P_i]]) 
        else:
            P_i = np.bmat([[I[0,0]*P_i, I[0,1]*P_i], [I[1,0]*P_i, I[1,1]*P_i]]) 
    return(P_i) 


#Heisenberg Hamiltonian 
def Hamiltonian(particles):
    J_ij = 1.0 #anistropy parameter
    B_j = 0.0 #local magnetic field

    #Chain
    H = np.zeros([2**particles,2**particles])

    #Loop
    #H = 0.5*J_ij*(spinoperatorplus(particles,1)*spinoperatorminus(particles,particles) + spinoperatorplus(particles,particles)*spinoperatorminus(particles,1)) + J_ij*(spinoperatorz(particles,1)*spinoperatorz(particles,particles))

    #Particles not interacting
    #H = -(0.5*J_ij*(spinoperatorplus(particles,2)*spinoperatorminus(particles,3) + spinoperatorplus(particles,3)*spinoperatorminus(particles,2)) + J_ij*(spinoperatorz(particles,2)*spinoperatorz(particles,3)))

    for i in range(particles-1):
	H_i = 0.5*J_ij*(spinoperatorplus(particles,i+1)*spinoperatorminus(particles,i+2) + spinoperatorplus(particles,i+2)*spinoperatorminus(particles,i+1)) + J_ij*(spinoperatorz(particles,i+1)*spinoperatorz(particles,i+2))
	H = H + H_i
    for j in range(particles):	
	H_j = B_j*spinoperatorz(particles, j+1)
	H = H + H_j
    return(H)

Ham = Hamiltonian(2)

w, v = la.eig(Ham)

#Computing eigenvalues of Hamiltonian
def eigenvalues(particles):
    for i in range(0, 2**particles):
	w_i = w[i] 
	return(round(w_i,4)) #eigenvalues
eigenvalues(2)   

#Computing column eigenvectors of Hamiltonian
def eigenvectorsc(particles):
    for i in range(0, 2**particles):
	v_i = v[i]
	vec = v_i.reshape(2**particles,1)
	print(np.around(vec, decimals=6)) #If have a print here it prints all eigenvectors but when there's a return it only prints one
    
eigenvectorsc(2)

print("----------------")

#Computing row eigenvectors of Hamiltonian
def eigenvectorsr(particles):
    for i in range(0, 2**particles):
	v_i = v[i] 
	return(np.around(v_i, decimals=6)) #eigenvalues
eigenvectorsr(2)

"""
#Computing expectation values
def expecval(particles):
    for i in range(particles):
        Ket_i = spinoperatorz(particles, i+1)*eigenvectorsc(particles)
        Bra_i = eigenvectorsr(particles)*Ket_i
    	print(Bra_i)
    
expecval(2)
