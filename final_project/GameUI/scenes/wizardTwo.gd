extends CharacterBody2D


const SPEED = 300.0
const JUMP_VELOCITY = -400.0

# shield status
var p2_shield_status = false

# Lightball stuff
const LIGHTBALL = preload("res://scenes/lighball.tscn")
const YELLOWBEAM = preload("res://scenes/p2_beam.tscn")


# animation Override
@onready var sprite2D = $Sprite2D
var animationOverride = false

# Beam status
var beamStatus= false

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

var P2_SHIELD = preload("res://scenes/p2_shield.tscn")

func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		velocity.y += gravity * delta

	## Handle jump.
	#if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		#velocity.y = JUMP_VELOCITY
#
	## Get the input direction and handle the movement/deceleration.
	## As good practice, you should replace UI actions with custom gameplay actions.
	#var direction = Input.get_axis("ui_left", "ui_right")
	#if direction:
		#velocity.x = direction * SPEED
	#else:
		#velocity.x = move_toward(velocity.x, 0, SPEED)
		
	

	move_and_slide()
	if (Input.is_action_just_pressed("p2_defend")):
		player2_defend(true)
		
	if(Input.is_action_just_pressed("p2_attack")):
		player2_attack()
		
	if(Input.is_action_just_pressed("p2_beam")):
		player2_beam(true)
		
	
	check_and_return_to_idle_animation(animationOverride)
	
	if(beamStatus):
		sendBeams()
		
func injury(damage):
	sprite2D.play("hurt")
	get_tree().get_root().get_node("Node").mqtt_injurePlayer(2, damage)
	
func player2_attack():
	sprite2D.animation = "attackSpell"
	var lightball = LIGHTBALL.instantiate()
	get_parent().add_child(lightball)
	lightball.position = $Marker2D.global_position

func player2_beam(newBeamState):
	if(newBeamState):
		sprite2D.animation = "beamAttack"
		animationOverride = true
		beamStatus= true
	else:
		beamStatus = false
		animationOverride = false

func sendBeams():
	var yellowBeam = YELLOWBEAM.instantiate()
	get_parent().add_child(yellowBeam)
	yellowBeam.position = $Marker2D.global_position
	
func player2_defend(new_shield_state):
	if(new_shield_state == true and p2_shield_status == false):
		sprite2D.play("deployShield")
		animationOverride = true
		var p2_shield = P2_SHIELD.instantiate()
		get_parent().add_child(p2_shield)
		p2_shield.position = $Marker2D.global_position
		p2_shield_status = true
	elif(new_shield_state == false):
		#Destroy the p1_shield child that was made above
		var shieldNode = get_parent().get_node_or_null("p2_shield")
		if shieldNode != null:  # Check if the p1_shield exists
			
			shieldNode.destroy()  # Destroy the p1_shield node
			p2_shield_status = false
			animationOverride = false

	
func check_and_return_to_idle_animation(override):
	if (sprite2D.is_playing() == false and override == false):
		sprite2D.animation="default"
		sprite2D.play("default")
		
func die():
	sprite2D.animation="dead"
	sprite2D.play("dead")
	animationOverride = true
	

	
