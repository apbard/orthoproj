# OrthogonalProjection
Easily create Orthogonal Projections graphs with matplotlib.

[Orthogonal Projections](https://en.wikipedia.org/wiki/Multiview_orthographic_projection) (or  Orthographic Projections) are 2D visualisations of 3D objects from different directions all parallel to one of the coordinate axes of the object. 
This class implements the first-angle scheme that is basically used worldwide but the United States (that uses the third-angle scheme) 

The following picture (taken from larapedia.com) show an example:
![proiezioni_ortogonali](https://cloud.githubusercontent.com/assets/12557177/15484325/ca1bf938-2139-11e6-9617-af6c9d92d9e5.jpg)


### Features

* All axes are synchronised
* Different kind of plot supported:
  * Plot
  * Scatter
  * Wireframe
  * Surface (in 2D subplots a wireframe is still shown)
  * Collection
* All arguments supported by underlying matplotlib plot are supported
* Blocking/Non Blocking show

### Documentation/Example 
See [orthoproj_demo.py](https://github.com/apbard/orthoproj/blob/master/examples/orthoproj_demo.py) to see an example that will produce the following plot:

![example](https://cloud.githubusercontent.com/assets/12557177/15484323/c9fd5adc-2139-11e6-81ae-0f400952de62.png)
