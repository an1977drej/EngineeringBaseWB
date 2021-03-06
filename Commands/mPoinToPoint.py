import FreeCAD
import FreeCADGui

import EB_Auxiliaries


class SelObserverPointToPoint:
    def __init__(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        print("Please select point on first object!")

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        # FreeCAD.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        # FreeCAD.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # FreeCAD.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # FreeCAD.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object

        if str(sub).startswith("Vertex"):
            objPoint = FreeCAD.Vector(pnt[0], pnt[1], pnt[2])
            self.stack.append([str(obj), objPoint])
        if len(self.stack) == 1:
            print("Please select point on second object!")
        if len(self.stack) == 2:
            ObjA_Name = self.stack[0][0]
            ObjB_Name = self.stack[1][0]
            PointA = self.stack[0][1]
            PointB = self.stack[1][1]
            Vector = PointB - PointA
            Pos0 = FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement.Base
            Rot0 = FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement.Rotation
            # Rot0 = App.ActiveDocument.getObject(ObjB_Name).Placement.Rotation
            MVector = Pos0 + Vector
            FreeCAD.ActiveDocument.openTransaction("Move Point to Point")
            FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement = FreeCAD.Placement(MVector, Rot0)
            FreeCAD.ActiveDocument.commitTransaction()
            print("First object -" + ObjA_Name + "- is moved!")
            RemoveObservers()
            self.stack = []


selGate = EB_Auxiliaries.SelectionGate("Vertex")
FreeCADGui.Selection.addSelectionGate(selGate)
observer = SelObserverPointToPoint()
FreeCADGui.Selection.addObserver(observer)


def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")
