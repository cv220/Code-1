# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 09:17:40 2025

@author: carson.vetsch
"""

#_______________________________________________
import math  # pulls a predefined extensive directory of python code

from linear_solver import solve_linear_system
#_______________________________________________
#_______________________________________________
def run_console_session():

    my_data_mgmt = Input_Mgmt(float)
    my_system = Lin_Solve()

    size = my_data_mgmt.ask_dimension()

    my_system.a = my_data_mgmt.read_matrix(size, "coefficient")
    my_system.b = my_data_mgmt.read_vector(size, "right-hand side")

    my_system.solve_lin_system()

    return my_system.a, my_system.b, my_system.x


def main():

    my_output = Output_Mgmt()

    coefficients, rhs, solution = run_console_session()

    print()

    print("Here is the system solution: ")
    print()

    my_output.display_matrix(coefficients)
    my_output.display_array(rhs)
    my_output.display_array(solution)

    my_output.store_to_file(solution)


    return


#______________________________________________
#______________________________________________
class Input_Mgmt( object ):

    def __init__( self, funct ):

        self.funct  = funct


#______________________________________________
    #______________________________________________
    def ask_dimension( self ):

        while True:

            try:

                dimension = int( input( "Enter the size of the square matrix (n): " ) )

            except ValueError:

                print( "Please enter an integer value for n." )
                continue

            if dimension <= 0:

                print( "Please enter a positive integer." )

            else:

                return dimension


    #_______________________________________________
    def read_matrix( self, size, description ):

        matrix = []

        for i in range( size ):

            row = []

            for j in range( size ):

                while True:

                    entry = input( f"Enter the { description } matrix entry at row { i + 1 }, column { j + 1 }: " )

                    try:

                        value = self.funct( entry )

                    except ValueError:

                        print( "Please enter a numeric value." )
                        continue

                    row.append( value )
                    break

            matrix.append( row )

        return matrix


    #_______________________________________________
    def read_vector( self, size, description ):

        vector = []

        for i in range( size ):

            while True:

                entry = input( f"Enter the { description } vector entry at position { i + 1 }: " )

                try:

                    value = self.funct( entry )

                except ValueError:

                    print( "Please enter a numeric value." )
                    continue

                vector.append( value )
                break

        return vector
#______________________________________________
class Lin_Solve( object ):
    
    def __init__( self ):
        
        self.a = [] #matrix
        self.b = [] #rhs
        self.x = [] #solve system
        
    #______________________________________________
    def test_data( self ):
        
        print( self.a )
        print( self.b )
        
    #______________________________________________
    #_______________________________________________
    def solve_lin_system( self ):
        
        a = self.a
        b = self.b

        self.x = solve_linear_system(a, b)

        return
    #_______________________________________________        
    
#______________________________________________
#______________________________________________
class Output_Mgmt( object ):
    
    
    def __init__( self ):
        
        
        pass
        
  
    #______________________________________________
    def display_array( self, array ):
        
        for row in array:    
            print( row ) # implicit loop (no counter) (fewer characers)
            
            
        print()
        
        return
    #______________________________________________
    #_______________________________________________
    def display_matrix( self, matrix ):
        
        
        for row in matrix:
            
            for entry in row:
            
                print( entry, end = " " ) 
            
            print()
            
        print()

        
        return
    #_______________________________________________
    #_______________________________________________
    def store_to_file( self, array ):
     
        file_name = input("Save solution array as: " )
        file_name = file_name + ".txt"
        
        external_file = open( file_name, "wt" ) # wt is keyword for write
        
        for row in array:
            
            string = str( row ) + "\n"
            
            external_file.write( string )
            
        external_file.close() # make sure to add bc otherwise it could get lost(stored in buffer temperarily before saving to file)
        
        
        return
    #_______________________________________________

    #_______________________________________________
    def store_mtrx_to_file( self, matrix ):
     
        file_name = file_name = input("Enter the matrix-file name: " )
        
        external_file = open( file_name, "wt" ) # wt is keyword for write
        
        for row in matrix:
            
            string = ""
            for entry in row:
                string = string + str( entry ) + " "
                
            string = string + "\n"
     
        
            external_file.write( string )
            
        external_file.close()
        
        
        return
    #_______________________________________________

#______________________________________________
#______________________________________________
if __name__ == "__main__":
    main()
#______________________________________________