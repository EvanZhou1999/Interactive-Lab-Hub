extends Area2D

var velocity = Vector2()
var SPEED = -1000
var movementPosition = 100



# Called when the node enters the scene tree for the first time.
func _ready():
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	if(global_position.x > get_parent().get_node("Player2/Marker2D").global_position.x - movementPosition):
		velocity.x = SPEED
		translate(velocity * delta)
		
func _on_visible_on_screen_notifier_2d_screen_exited():
	queue_free()

func destroy():
	queue_free()


