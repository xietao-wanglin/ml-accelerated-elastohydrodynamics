import unittest
from unittest import TestCase

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import axes3d

from simulation import Simulation

class TestFlow(TestCase):
    
    def test_single_dumbbell_flow(self):

        sim = Simulation()
        x_flat = np.linspace(-1, 1, 100)
        y_flat = np.linspace(-1, 1, 100)
        X = np.meshgrid(x_flat, y_flat)
        U = sim.fluid_flow(X)
        u, v = U[..., 0], U[..., 1]
        x, y = X
        plt.plot(sim.bead_pos[:, 0], sim.bead_pos[:, 1],
                                marker='o', lw=4)
        plt.streamplot(x, y, u, v, color='red')
        plt.pcolormesh(x, y, np.sqrt(u*u+v*v), alpha=1, cmap='PiYG',
                                      norm=colors.LogNorm(vmin=0.001, vmax=100))
        plt.show()

    def test_three_dumbbell_flow(self):

        r = np.array([[ 0.72771121, +0.76493629],
            [ 0.03475821, -0.73586379],
            [ 0.83371936, +0.20788059],
            [ 0.13084262, -0.63344033],
            [-0.71030448, -0.8388744],
            [-0.28877452,  0.88086389]])
        sim = Simulation(bead_pos=r)
        x_flat = np.linspace(-1, 1, 100)
        y_flat = np.linspace(-1, 1, 100)
        X = np.meshgrid(x_flat, y_flat)
        U = sim.fluid_flow(X)
        u, v = U[..., 0], U[..., 1]
        x, y = X
        plt.streamplot(x, y, u, v, color='red')
        plt.pcolormesh(x, y, np.sqrt(u*u+v*v), alpha=1, cmap='PiYG',
                                      norm=colors.LogNorm(vmin=1e-2, vmax=10))
        plt.show()

    def test_animation_single_dumbbell(self):

        sim = Simulation(shear=1)
        sim.solve_dynamics(max_time=10.0, verbose=True)
        sim.create_2d_animation(filename='test_2d.mp4')

    def test_animation_three_dumbbell(self):

        r = np.array([[ 0.72771121, +0.76493629],
            [ 0.03475821, -0.73586379],
            [ 0.83371936, +0.20788059],
            [ 0.13084262, -0.63344033],
            [-0.71030448, -0.8388744],
            [-0.28877452,  0.88086389]])
        sim = Simulation(bead_pos=r)
        sim.solve_dynamics(max_time=20.0, verbose=True)
        sim.create_2d_animation(domain=[[-3, -3], [3, 3]])

    def test_3d_single_dumbbell_flow(self):

        r = np.array([[0, 0.5, 0], 
                      [0, -0.5, 0]])
        sim = Simulation(bead_pos=r, shear=1)

        ax = plt.figure().add_subplot(projection='3d')

        x_flat = np.linspace(-1, 1, 10)
        y_flat = np.linspace(-1, 1, 10)
        z_flat = np.linspace(-1, 1, 10)
        X = np.meshgrid(x_flat, y_flat, z_flat)
        U = sim.fluid_flow(X)
        u, v, w = U[..., 0], U[..., 1], U[..., 2]
        x, y, z = X

        ax.quiver(x, y, z, u, v, w, color='r', length=10)
        ax.plot(sim.bead_pos[:, 0], sim.bead_pos[:, 1], zs=sim.bead_pos[:, 2], marker='o')
        plt.show()

    def test_3d_animation_single_dumbbell(self):

        r = np.array([[0, 0.5, 0], 
                      [0, -0.5, 0]])
        sim = Simulation(bead_pos=r, shear=1)
        sim.solve_dynamics(max_time=10.0, verbose=True, method='Radau')
        sim.create_3d_animation(domain=[[-1, -1, -1], [1, 1, 1]], arrow_size=10, filename='test_3d.mp4')

    def test_3d_animation_three_dumbbell(self):

        r = np.array([[ 0.72771121, +0.76493629, 0.2],
            [ 0.03475821, -0.73586379, 0.2],
            [ 0.83371936, +0.20788059, 0],
            [ 0.13084262, -0.63344033, 0],
            [-0.71030448, -0.8388744, -0.3],
            [-0.28877452,  0.88086389, -0.45]])
        sim = Simulation(bead_pos=r)
        sim.solve_dynamics(max_time=20.0, verbose=True)
        sim.create_3d_animation(domain=[[-3, -3, -3], [3, 3, 3]])
