extends Area2D

const SPEED = 900
var velocity = Vector2()



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	velocity.x = SPEED * delta
	translate(velocity)


func _on_visible_on_screen_notifier_2d_screen_exited():
	queue_free()


func _on_body_entered(body):
	print(body.name)
	if(body.name == "Player2"):
		body.injury(1)
	queue_free()


func _on_area_entered(area):
	if(area.name == "p2_shield"):
		get_tree().get_root().get_node("Node").mqtt_successfulDefend(2)
		queue_free()
	
