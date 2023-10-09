Symbols used in Derivations
###########################

TikZ
****

This is a test of tikz

.. tikzimage:: An Example TikZ Directive with Caption
   :align: center

   \draw[thick,rounded corners=8pt]
   (0,0)--(0,2)--(1,3.25)--(2,2)--(2,0)--(0,2)--(2,2)--(0,0)--(2,0);

Volume Integral
***************

..  math::

     \newcommand{\oiiint}{{\Large{\subset\!\supset}} \llap{\iiint}}
     \oiiint_V

..  note::

    This is not "pretty". It needs to be replaced with a *MathJax* compatible
    verison later.

Surface Integral
****************

..  math::


    \newcommand{\oiint}{{\subset\!\supset} \llap{\iint}}
    \oiint_S

Gradiant
********

   The gradient of a function :math:`\mathbf{f}` at point :math:`a` is:
   
..  math::

    \overrightarrow{\nabla} \mathbf{f}(a)

The resulting vector indicates the direction and the maximum rate of increase
of the function at the specified point. 

Flux
****

Let :math:`\mathbf{q}` be a quantity that can move, like mass, energy, or momentum. Now define :math:`\rho` as the density of that quantity per unit volume.  Let :math:`R` be an arbitrary volume, bounded by a closed surface :math:`S`, then the *flux* 

Divergence Theorem
******************

..  math::
    \newcommand{\oiint}{{\subset\!\supset} \llap{\iint}}
    \newcommand{\oiiint}{{\Large{\subset\!\supset}} \llap{\iiint}}

    \oiiint_V (\nabla\cdot\overrightarrow{\mathbf{F}}dV =
    \oiint_S(\mathbf{F}\cdot\overrightarrow{\mathbf{n}} dS

..  tikzimage::  Arbitrary Volume
    :tikzlibs: calc, intersections
    :align: center
    :width: 300



    \shadedraw[ball color=gray!40,opacity=0.5] plot[smooth cycle] 
    coordinates {(-2,1) (-0.8,2.2) (0.5,1.3) (1,0.8) (1.8,0)
    (2,-1) (1.4,-2) (0,-2.1) (-1,-1.7) (-1.8,-1)};
    \draw[fill=gray!40] (0.8,0) to[bend right=10] 
        (1.3,0.3) to[bend left=15] (1.6,-0.3)
        to[bend left=10] (1.2,-0.6) to[bend right=10] cycle;
    \draw[blue,very thick,-latex] (1.2,-0.1) -- ++(38:1) 
        node[above] {$\overrightarrow{ds}$};
    \node[anchor=north] at (1.3,-0.6) {d$S$}; 
    \node[anchor=north] at (-0.8,0.6) {$R$}; 
    \draw[fill=gray!40] (-0.8,-0.8) rectangle (-0.3,-1.3) node[below right=0pt,
        inner sep=0pt]{d$R$};

