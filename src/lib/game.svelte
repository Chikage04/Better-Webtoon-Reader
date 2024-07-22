<script>
  import { onMount } from 'svelte';
  let game;
  let Phaser;

  onMount(async () => {
    Phaser = await import('phaser');

    const config = {
      type: Phaser.AUTO,
      width: 800,
      height: 600,
      physics: {
        default: 'arcade',
        arcade: {
          gravity: { y: 300 },
          debug: false
        }
      },
      scene: {
        preload: preload,
        create: create,
        update: update
      }
    };

    // Attendre une interaction de l'utilisateur pour démarrer le jeu
    window.addEventListener('click', () => {
      if (!game) {
        game = new Phaser.Game(config);
      }
    });

    function preload() {
      // Pas besoin de précharger les images car nous utilisons des graphiques
    }

    function create() {
      // Créer un fond bleu
      this.add.rectangle(400, 300, 800, 600, 0x87CEEB).setScrollFactor(0);

      // Créer des plateformes statiques
      this.platforms = this.physics.add.staticGroup();
      createPlatform.call(this, 400, 568, 800, 32);

      // Créer le joueur (un carré rouge)
      this.player = this.add.rectangle(100, 450, 32, 32, 0xFF0000);
      this.physics.add.existing(this.player);
      this.player.body.setCollideWorldBounds(true);
      this.player.body.setGravityY(300);
      this.player.body.setBounce(0.2);

      // Ajouter les collisions entre le joueur et les plateformes
      this.physics.add.collider(this.player, this.platforms);

      // Définir les contrôles du clavier
      this.cursors = this.input.keyboard.createCursorKeys();

      // Configurer la caméra pour qu'elle suive le joueur avec un léger retard
      this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
      this.cameras.main.setBounds(0, 0, Number.MAX_SAFE_INTEGER, 600);

      this.nextPlatformX = 800; // Position X pour la prochaine plateforme
    }

    function update() {
      // Réinitialiser la vélocité horizontale du joueur
      this.player.body.setVelocityX(0);

      if (this.cursors.left.isDown) {
        // Déplacer à gauche
        this.player.body.setVelocityX(-160);
      } else if (this.cursors.right.isDown) {
        // Déplacer à droite
        this.player.body.setVelocityX(160);
      }

      // Permettre de sauter si le joueur touche le sol
      if (this.cursors.up.isDown && this.player.body.touching.down) {
        this.player.body.setVelocityY(-330);
      }

      // Ajouter des plateformes à mesure que le joueur avance
      if (this.player.x > this.nextPlatformX - 800) {
        createPlatform.call(this, 600, 568, 800, 32);
        this.nextPlatformX += 800;
      }
    }

    function createPlatform(x, y, width, height) {
      const platform = this.add.rectangle(x, y, width, height, 0x00FF00);
      this.physics.add.existing(platform, true);
      this.platforms.add(platform);
    }

    return () => {
      if (game) {
        game.destroy(true);
      }
    };
  });
</script>

<div id="phaser-game"></div>

<style>
  #phaser-game {
    width: 100%;
    height: 100%;
  }
</style>
