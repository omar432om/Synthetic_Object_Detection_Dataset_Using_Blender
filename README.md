# Using 3D models to create synthetic data using Blender for object detection and tracking

This project is an example of the usage of Blender to create synthetic training dataset to train computer vision models for multiple moving objects detection and counting. The advantages of such a technique compared to the standard dataset creating methods (taking real life pictures and manually labeling them):

 - Saving time.
  - Expirementing with diffirent object sizes and shapes and speeds and numbers.
  - Expirementing with diffirent enviroment conditions like lighting and weather and background conditions.
  - Can be used for transfer learning, reducing the amount of real life data needed.
  - Testing the applicability of the project before investing time and money in real life data collecting and labeling.
  
The main reason for using this method is not for training a final NN model. Instead, it is for experimenting on different dataset conditions and NN architectures to determine the most suitable model to implement. The final model can be then trained or fine-tuned using transfer learning with real life data.

# A simple project to illustrate the usefulness of synthetic training data: Stones Counter.

The project will go through the following steps:
-	Creating Blender 3D model of the problem.
-	Programing Blender to automatically render the frames and output .txt file with the bounding boxes in COCO format.
-	Divide the generated data into training and validation and testing sets.
-	Training the object detection NN using the generated training dataset and test it using the testing dataset.
the 3D model or the NN can be then modified depending on the results and the previous steps can be repeated again in short time.

Before going forward, import all included .py files into blender by going to Scripting Veiw and pressing Open under the text editor. Then you can choose the .py files you wish to import.

------------------------------------------
# First: Creating the 3D model using blender. (Blender 2.79 must be used) 

Blender provides a tool to generate particles and easily control their speed and sizes and direction and randomize them within your desired range. This will be used to generate multiple stones moving with random speeds and have random colors and sizes and rotations. We add a source and then add a particle system to it:

![1](https://user-images.githubusercontent.com/50550592/103855454-c3dfc900-50c3-11eb-873d-e6bc2cd0800c.PNG)

We can see in the previous image the emitter (source of particles) and the emitted particles and the reference object (stone). We can then modify the particles properties using the following tab in the emitter settings:

![2](https://user-images.githubusercontent.com/50550592/103855212-3ef4af80-50c3-11eb-8610-b2813b6f5b15.PNG)

For more information regarding working with particles in Blender, watch this  [tutorial by Remington Creative](https://www.youtube.com/watch?v=6p74pEH-k8s)
And this [tutorial by Blender Know How](https://www.youtube.com/watch?v=9vEoBUnMXh4&feature=youtu.be)

The generated particles are then converted into objects using a modified version of [copy_particles_to_sim.py by Eli Spizzichino](https://gist.github.com/diramazioni/6170712) in order to be able to get their bounding boxes later. The attached CopyParticles.py causes multiple errors with Blender 2.80 and above, so it is recommended to use Blender 2.79 for making the particles and converting them to objects using CopyParticles.py. After this you should save the .blend file and work on it with Blender 2.80 as this is the version I have tested the following steps and codes on.

We then add a camera and lighting source and a background. We can also add multiple sources from different directions:

![3](https://user-images.githubusercontent.com/50550592/103856893-7b75da80-50c6-11eb-8cc1-563b605e8d9a.PNG)

We can also randomize the colors of the emitted particles using Blender nodes. To learn how, Watch this [tutorial by 
Steven Scott](https://www.youtube.com/watch?v=CuA1cn77Iuo&feature=youtu.be)

The background can also be changed by just moving the background object each few frames to prevent overfitting in training our NN.

-------------------------------------------
# Second: Programing Blender to automatically render the frames and output .txt file with the bounding boxes in COCO format.

The script used is based on the script used in [Tensorflow Garbage Classifier](https://github.com/olestourko/ml-garbage-classifier-tensorflow/tree/master/blender-data-generator). But I made modifications were made to enable the script to work with newer versions of Blender (2.80) and to work when the stones are not visible in the scene at some frames. And added an additional annotation format (COCO) due to its high popularity in machine vision. The edited scripts I used can be found in this project files (Annotations.py). If you want to use them make sure to change the directories and object names and output files names to match your project.Also, please copy the attached labels.json and cache.json into your chosen output folder before running Annotations.py. I made them to enable the user to render a desired number of frames and the code will continue to render any aditional frames when you run it again, starting from where it stopped last time automatecly and adding the bounding boxes to the same previousely created labels.json file. 

-------------------------------

# Third: Viewing the bounding boxes and dividing the dataset into train/validation/test sets and train our NN

There are multiple available methods which can be used to perform these steps similar to the regular way used with real life data. For the sake of illustration, Roboflow website can be used to perform them easily. You can watch this [Roboflow tutoial](https://www.youtube.com/watch?v=_9vGiEs3W9Y) to learn how to visualize your dataset and change its format and use it to train different  pre-implemented NNs and test their performances.

-------------------
# Samples from the annotated training set:
![4](https://user-images.githubusercontent.com/50550592/103861542-ac5a0d80-50ce-11eb-8739-7fcfea0ad13e.png)
![5](https://user-images.githubusercontent.com/50550592/103861548-ae23d100-50ce-11eb-9d66-81a57642ff19.PNG)
---------------------
# Samples from the detected stones in the test set using YOLO V4:
![6](https://user-images.githubusercontent.com/50550592/103861556-af54fe00-50ce-11eb-91ad-3f3f4e4c28c3.png)
![7](https://user-images.githubusercontent.com/50550592/103861558-afed9480-50ce-11eb-9c4c-b767dfffa25b.png)
-------------------------------------------------


