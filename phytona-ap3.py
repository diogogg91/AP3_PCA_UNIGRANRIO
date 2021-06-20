import pygame
import pygame.freetype



class SimpleScene:
    FONT = None

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('black'))

        y = 80
        if text:
            if SimpleScene.FONT == None:
                SimpleScene.FONT = pygame.freetype.SysFont(None, 22)
            for line in text:
                SimpleScene.FONT.render_to(self.background, (300, y), line, pygame.Color('black'))
                SimpleScene.FONT.render_to(self.background, (25, y - 1), line, pygame.Color('white'))
                y += 50

        self.next_scene = next_scene
        self.additional_text = None

    def start(self, text):
        self.additional_text = text

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if self.additional_text:
            y = 180
            for line in self.additional_text:
                SimpleScene.FONT.render_to(screen, (120, y), line, pygame.Color('black'))
                SimpleScene.FONT.render_to(screen, (110, y - 1), line, pygame.Color('white'))
                y += 50

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return (self.next_scene, None)


class GameState:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        # CHANGE
        self.questions = [
            ("Em que ano o phyton foi criado?", 1),
            ("Quem criou o Python?", 2),
            ("O phyton é gerenciado por quem ?", 3),
            ("Em Python, strings são ... ? ?", 4),
            ("Qual desses é uma linguagem de programação?", 4),
            ("Qual o formato principal de declarar string no Python ?", 1),
            ("São imutáveis.", 2),
        ]
        self.current_question = None

        # CHANGE
        self.question_index = 0

        self.right = 0
        self.wrong = 0

    def pop_question(self):
        q = self.questions[0]
        self.questions.remove(q)
        self.current_question = q

        # CHANGE
        self.question_index += 1

        return q

    def answer(self, answer):
        if answer == self.current_question[1]:
            self.right += 1
        else:
            self.wrong += 1

    def get_result(self):
        return f'{self.right} Acerto', f'{self.wrong} Erro', '', 'Muito Bom!' if self.right > self.wrong else 'Pode melhorar!'


class SettingScene:

    def __init__(self):

        width = 800
        height = 600

        self.background = pygame.Surface((width, height))
        self.background.fill(pygame.Color('black'))

        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)

        SimpleScene.FONT.render_to(self.background, (120, 50), 'grau de dificuldade', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (119, 49), 'grau de dificuldade', pygame.Color('white'))

        self.rects = []

        # CHANGE
        for n in range(4):
            rect = pygame.Rect(50, (n * 70) + 100, 500, 50)
            self.rects.append(rect)

    def start(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('black'), rect)
            pygame.draw.rect(screen, pygame.Color('black'), rect, 5)

            # CHANGE
            SimpleScene.FONT.render_to(screen, (rect.x + 30, rect.y + 15), str(n), pygame.Color('black'))
            SimpleScene.FONT.render_to(screen, (rect.x + 29, rect.y + 14), str(n), pygame.Color('white'))

            n += 1

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        return ('GAME', GameState(n))
                    n += 1


class GameScene:
    def __init__(self):
        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 28)

        self.rects = []

        for n in range(4):
            rect = pygame.Rect(50, (n * 70) + 100, 500, 50)
            self.rects.append(rect)

        # CHANGE
        self.choices = (
            ['1989', '1990', '1991', '1992', '1993'],
            ["Oliver Jack", "Guido van Rossum", "Harry Connor", "Jacob Michael"],
            ["Python Foundation", "Python Software ", "Python Software Foundation", "Software Foundation", "Software Foundation Phyton"],
            ['mutável', 'imutável', 'matrizes', 'STR objetos'],
            ['Firefox', ' Explorer', 'Chrome', 'Phyton', 'Safari'],
            ['Aspas simples e Aspas duplas', 'Aspas simples e Parênteses', 'Aspas duplas e Hashtags', 'Aspas duplas e Parênteses', 'Hashtags e Parênteses'],
            ['Operador', 'Tupla', 'Classe', 'Dicionário']
        )

    def start(self, gamestate):
        self.background = pygame.Surface((720, 480))
        self.background.fill(pygame.Color('black'))
        self.gamestate = gamestate
        question, answer = gamestate.pop_question()
        SimpleScene.FONT.render_to(self.background, (120, 50), question, pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (119, 49), question, pygame.Color('white'))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 0
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('black'), rect)
            pygame.draw.rect(screen, pygame.Color('black'),
                             rect, 5)

            # CHANGE
            for i in range(len(self.choices)):
                if self.gamestate.question_index == i + 1:
                    SimpleScene.FONT.render_to(screen, (rect.x + 30, rect.y + 20), str(self.choices[i][n]),
                                               pygame.Color('black'))
                    SimpleScene.FONT.render_to(screen, (rect.x + 29, rect.y + 19), str(self.choices[i][n]),
                                               pygame.Color('white'))
            n += 1

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        self.gamestate.answer(n)
                        if self.gamestate.questions:
                            return ('GAME', self.gamestate)
                        else:
                            return ('RESULT', self.gamestate.get_result())
                    n += 1


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    dt = 0
    scenes = {
        'TITLE': SimpleScene('SETTING', 'QUIZ EM PHYTON', '', '', '', 'APERTE [ESPAÇO]'),
        'SETTING': SettingScene(),
        'GAME': GameScene(),
        'RESULT': SimpleScene('TITLE', 'RESULTADO:'),
    }
    scene = scenes['TITLE']
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)

        scene.draw(screen)
        

        pygame.display.flip()
        dt = clock.tick(60)


if __name__ == '__main__':
    main()
