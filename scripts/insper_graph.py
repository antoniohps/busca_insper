# encoding: utf-8

import math
import numpy as np
import matplotlib.pyplot as plt

def nb_draw_map(occ_grid, ax = None, particles = None, pose=False, robot=False, robot_radius=.5, dest=None):
    """
        particles - um conjunto de partículas definidas como objetos do tipo partícula

        initial_position - cor para desenhar a posição inicial do robo

        pose - pose do robo

        robot - booleano que determina se o robô é desenhado como um círculo ou não
    """
    mapa_numpy = 255 - occ_grid.grid

    ax = nb_overlay(mapa_numpy, occ_grid, ax=ax)

    if particles:
        nb_draw_particle_cloud(particles, ax)
    if pose:
        nb_draw_arrow(pose[0], pose[1], pose[2], ax, l=robot_radius, color='g')
    if robot:
        nb_draw_robot(pose, ax, radius=robot_radius)
    if dest:
        nb_draw_cross(dest[0], dest[1], ax)

    return ax # Retornamos o contexto grafico caso queiram fazer algo depois

def nb_overlay(numpy_img, occ_grid, ax=None, alpha=1.):
    
    height, width = occ_grid.height, occ_grid.width
    or_x, or_y = occ_grid.origin_x, occ_grid.origin_y
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10,10))
        ax.set(xlim=[or_x, or_x + width], ylim=[or_y, or_y + height]) # Or use "ax.axis([x0,x1,y0,y1])"
        fig.canvas.draw()

    if len(numpy_img.shape) > 2:
        ax.imshow(numpy_img, alpha=alpha, origin='lower', extent=(or_x, or_x + width, or_y, or_y + height))
    else :
        ax.imshow(numpy_img, cmap="gray", alpha=alpha, origin='lower', extent=(or_x, or_x + width, or_y, or_y + height))

    return ax # Retornamos o contexto grafico caso queiram fazer algo depois

def nb_draw_initial_pose(pose_xytheta, ax):
    """
        Metodo que desenha a pose inicial
        pose - um array que contem x, y e theta da pose inicial
        ax - um objeto do matplotlib
    """
    x = pose_xytheta[0]
    y = pose_xytheta[1]
    theta = pose_xytheta[2]
    l = 15
    #end_x = x + deltax
    #end_y = y + deltay
    nb_draw_arrow(x, y, theta, ax, l=l, color='r', width=2, headwidth=6, headlength=6)

def nb_draw_arrow(x, y, theta, ax, l = 15, color='y', headwidth=3.0, headlength=3, width=0.001):
    """
        Desenha uma seta na posição x, y com um ângulo theta
        ax é o contexto gráfico

    """
    deltax = l*math.cos(theta)
    deltay = l*math.sin(theta)
    #ax.arrow(x, y, deltax, deltay, head_width=headwidth, head_length=headlength, fc=color,  ec=color, width=width)
    ax.arrow(x, y, deltax, deltay, fc=color,  ec=color, width=width)

def nb_draw_cross(x, y, ax, color='red', markersize=20):
    """
        Desenha uma seta na posição x, y com um ângulo theta
        ax é o contexto gráfico

    """
    ax.plot(x, y, color, marker='x', linestyle='None', markersize=markersize)


def nb_draw_particle_cloud(particles, ax):
    """
        Desenha o particle cloud
        particles - uma lista de objetos Particle
        ax - eixo
    """
    for p in particles:
        figx, figy, figt = convert_to_figure(np.array((p.x, p.y, p.theta)))
        nb_draw_arrow(figx, figy, figt, ax, particle_size, color='b')


def nb_draw_robot(pose, ax, radius=10):
    """
        Desenha um círculo com uma seta para se passar pelo robô
    """
    from matplotlib.patches import Circle

    posx, posy, post = pose
    circle = Circle((posx, posy), radius, facecolor='none',
                    edgecolor=(0.0, 0.8, 0.2), linewidth=2, alpha=0.7)
    ax.add_patch(circle)

