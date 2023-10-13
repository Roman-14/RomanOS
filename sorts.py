import pygame
import assets
import random
import threading
import time
import numpy as np
import sounddevice as sd

class Sort:
    def __init__(self, type, screen, quantity=100, delay=0.01) -> None:
        self.type = "Sort"
        if quantity>380:
            self.type = "None"
        self.x = 100
        self.y = 100
        self.w = 600
        self.h = 400

        self.rect = pygame.Rect((self.x, self.y, self.w, self.h))
        self.bar = pygame.Rect(self.x, self.y, self.w, 10)
        self.exitRect = pygame.Rect(self.x + self.w - 8, self.y + 3, 5, 5)

        
        self.quantity = quantity

        self.running = True

        self.items = [i + 1 for i in range(self.quantity)]
        random.shuffle(self.items)

        self.screen = screen
        self.delay = delay
        self.current_iterations = set()  # To keep track of the current iterations

        if type=="insertion":
            threading.Thread(target=self.insertionSort).start()
        elif type=="bubble":
            threading.Thread(target=self.bubbleSort).start()
        elif type == "merge":
            threading.Thread(target=self.mergeSort).start()
        elif type == "quick":
            threading.Thread(target=self.quickSort).start()
        elif type == "bogo":
            threading.Thread(target=self.bogoSort).start()
        elif type == "comb":
            threading.Thread(target=self.combSort).start()
        elif type == "cocktail":
            threading.Thread(target=self.cocktailShakerSort).start()
        elif type == "radix":
            threading.Thread(target=self.radixSort).start()
    def radixSort(self) -> None:
        max_value = max(self.items)
        exp = 1
        n = len(self.items)

        while max_value // exp > 0 and self.running:
            count = [0] * 10
            output = [0] * n

            for i in range(n):
                index = (self.items[i] // exp) % 10
                count[index] += 1

            for i in range(1, 10):
                count[i] += count[i - 1]

            i = n - 1
            while i >= 0:
                index = (self.items[i] // exp) % 10
                output[count[index] - 1] = self.items[i]
                count[index] -= 1
                i -= 1

            for i in range(n):
                if not self.running:
                    return
                self.items[i] = output[i]
                self.current_iterations = {i}
                time.sleep(self.delay)

            exp *= 10

        self.current_iterations = set()
        self.draw(self.screen, True)

    def cocktailShakerSort(self) -> None:
        left, right = 0, len(self.items) - 1
        swapped = True

        while swapped and self.running:
            swapped = False

            # Traverse from left to right, like a bubble sort
            for i in range(left, right):
                if not self.running:
                    return
                if self.items[i] > self.items[i + 1]:
                    self.items[i], self.items[i + 1] = self.items[i + 1], self.items[i]
                    swapped = True
                    self.current_iterations = {i, i + 1}
                    time.sleep(self.delay)

            if not swapped:
                break

            swapped = False
            right -= 1

            # Traverse from right to left
            for i in range(right, left, -1):
                if not self.running:
                    return
                if self.items[i] < self.items[i - 1]:  # Fixed the comparison here
                    self.items[i], self.items[i - 1] = self.items[i - 1], self.items[i]
                    swapped = True
                    self.current_iterations = {i, i - 1}
                    time.sleep(self.delay)

            left += 1

        self.current_iterations = set()
        self.draw(self.screen,True)
    def combSort(self) -> None:
        def get_next_gap(gap):
            gap = (gap * 10) // 13  # Reduce the gap by a factor of 1.3 (tuned for efficiency)
            if gap < 1:
                return 1
            return gap

        gap = len(self.items)
        swapped = True

        while self.running and (gap > 1 or swapped):
            gap = get_next_gap(gap)
            swapped = False

            for i in range(0, len(self.items) - gap):
                j = i + gap
                if self.items[i] > self.items[j]:
                    self.items[i], self.items[j] = self.items[j], self.items[i]
                    swapped = True
                    self.current_iterations = {i, j}
                    time.sleep(self.delay)

        self.draw(self.screen, True)
        self.current_iterations = set()

    def bogoSort(self) -> None:
        def is_sorted(arr):
            for i in range(1, len(arr)):
                if arr[i - 1] > arr[i]:
                    return False
            return True

        while not is_sorted(self.items) and self.running:
            random.shuffle(self.items)
            time.sleep(self.delay)

        self.draw(self.screen, True)

    def bubbleSort(self) -> None:
        self.running = True
        localrunning = True
        while self.running and localrunning:
            time.sleep(self.delay)
            before = self.items[:]
            for j in range(len(self.items) - 1):
                if self.items[j] > self.items[j + 1]:
                    temp = self.items[:]
                    temp2 = self.items[j]
                    temp[j] = self.items[j + 1]
                    temp[j + 1] = temp2
                    self.items = temp
                    self.current_iterations = {j, j + 1}  # Update the current iterations

            if before == self.items:
                self.draw(self.screen, True)
                self.current_iterations = set()
                localrunning = False
    def insertionSort(self) -> None:
        self.running = True
        for i in range(1, len(self.items)):
            if not self.running:
                break
            key = self.items[i]
            j = i - 1
            while j >= 0 and key < self.items[j] and self.running:
                self.items[j + 1] = self.items[j]
                j -= 1
                self.current_iterations = {j + 1, i}  # Update the current iterations

                time.sleep(self.delay)

            self.items[j + 1] = key
            time.sleep(self.delay)

        self.draw(self.screen, True)
        self.current_iterations = set()

    def quickSort(self) -> None:
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if not self.running:
                    break
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    self.current_iterations = {i, j}
                    time.sleep(self.delay)
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            self.current_iterations = {i + 1, high}
            time.sleep(self.delay)
            return i + 1

        def quickSortHelper(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quickSortHelper(arr, low, pi - 1)
                quickSortHelper(arr, pi + 1, high)

        quickSortHelper(self.items, 0, self.quantity - 1)
        self.draw(self.screen, True)
        self.current_iterations = set()

    def mergeSort(self) -> None:
        def merge(arr, left, right, mid):
            i = left
            j = mid + 1
            temp = []
            merged_indices = set()  # Store the indices that have already been merged

            while i <= mid and j <= right and self.running:
                if arr[i] <= arr[j]:
                    temp.append(arr[i])
                    i += 1
                else:
                    temp.append(arr[j])
                    j += 1

            while i <= mid:
                temp.append(arr[i])
                i += 1

            while j <= right:
                temp.append(arr[j])
                j += 1

            # Update the merged_indices set
            for k in range(left, right + 1):
                if k not in merged_indices:
                    merged_indices.add(k)

            self.items[left:right + 1] = temp

            # Update self.current_iterations with the merged_indices
            self.current_iterations = merged_indices
            time.sleep(self.delay)





        def mergeSortHelper(left, right):
            if left < right:
                mid = (left + right) // 2
                mergeSortHelper(left, mid)
                mergeSortHelper(mid + 1, right)
                merge(self.items, left, right, mid)

        mergeSortHelper(0, self.quantity - 1)
        self.draw(self.screen, True)
        self.current_iterations = set()

    def draw(self, screen, check=False):
        if self.running:
            pygame.draw.rect(screen, (70, 70, 70), self.rect)
            pygame.draw.rect(screen, (0, 0, 0), self.bar)
            pygame.draw.rect(screen, (255, 0, 0), self.exitRect)
        
        c = self.x
        self.perm = check
        
        rect_width = self.w / self.quantity
        rect_height = (self.h - 30) / len(self.items)
        
        if rect_width < 1:
            rect_width = 1
        if rect_height < 1:
            rect_height = 1

        if not check and not self.perm and self.running:
            for i in range(len(self.items)):
                if i in self.current_iterations:
                    pygame.draw.rect(self.screen, (255, 0, 0),
                                    (c, self.y + self.h - int(rect_height * self.items[i]) - 5, int(rect_width), int(rect_height * self.items[i]))
                    )
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                    (c, self.y + self.h - int(rect_height * self.items[i]) - 5, int(rect_width), int(rect_height * self.items[i])
                    ))
                c += rect_width
        elif self.running:
            self.current_iterations = {}
            for i in self.items:
                time.sleep(0.001)
                pygame.draw.rect(self.screen, (100, 255, 100),
                                (c, self.y + self.h - int(rect_height * i) - 5, int(rect_width), int(rect_height * i))
                )
                c += rect_width

    def mbHeld(self, mousePos):
        self.x = mousePos[0]
        self.y = mousePos[1]

        if (self.x + self.w) >= self.screen.get_rect().w:
            self.x = self.screen.get_rect().w - self.w
        elif self.x <= 0:
            self.x = 0
        if (self.y + self.h) >= self.screen.get_rect().h:
            self.y = self.screen.get_rect().h - self.h
        elif self.y <= 0:
            self.y = 0

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.bar = pygame.Rect(self.x, self.y, self.w, 10)
        self.exitRect = pygame.Rect(self.x + self.w - 8, self.y + 3, 5, 5)
