use rand::Rng;
use std::time::Instant;

/// Quicksort algorithm implementation
fn quicksort(arr: Vec<i32>) -> Vec<i32> {
    if arr.len() <= 1 {
        return arr;
    }

    let pivot = arr[arr.len() / 2];
    let mut left = Vec::new();
    let mut middle = Vec::new();
    let mut right = Vec::new();

    for &x in &arr {
        if x < pivot {
            left.push(x);
        } else if x == pivot {
            middle.push(x);
        } else {
            right.push(x);
        }
    }

    let mut result = quicksort(left);
    result.extend(middle);
    result.extend(quicksort(right));
    result
}

/// Verify if array is sorted
fn is_sorted(arr: &[i32]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

/// Run sorting benchmark with 100,000 random integers
pub fn run_benchmark() {
    let mut rng = rand::thread_rng();
    
    // Generate 100,000 random integers
    let arr: Vec<i32> = (0..100000).map(|_| rng.gen_range(0..1000000)).collect();

    // Measure sorting time
    let start_time = Instant::now();
    let sorted_arr = quicksort(arr.clone());
    let execution_time = start_time.elapsed().as_millis();

    // Verify sorting correctness
    let correct = is_sorted(&sorted_arr);

    println!("Test: Sorting (Quicksort)");
    println!("Array size: {}", arr.len());
    println!("Execution time: {} ms", execution_time);
    println!("Correctly sorted: {}", correct);
}
