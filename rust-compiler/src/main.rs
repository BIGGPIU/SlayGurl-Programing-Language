use std::{env::{args, current_dir}, time::Duration};


fn main() {

    
    let mut args:Vec<String> = args().collect();
    
    let delulu_status = rand::random_bool(0.1);

    if delulu_status == true {
        unsafe {
            let mut x = [0,0,0,0,0];
            let epic_gamer_x = x.as_mut_ptr();
            let mut i = 0;
            loop {

                epic_gamer_x.offset(6);
                epic_gamer_x.write_volatile(0xff_i32);
            
                if i == 999 {
                    panic!("There was a memory leak in the python program that language is unsafe gng...");
                    break;
                }
                i+=1;
            }
        }
    }

    // std::thread::sleep(Duration::from_millis(500));
    println!("Compiling 12,000 packages");
    println!("[===============> ] 952/1200");
    std::thread::sleep(Duration::from_millis(500));
    println!("Compiling 12,000 packages");
    println!("[================>] 1200/1200");
    std::thread::sleep(Duration::from_millis(1000));
    println!("\n\n");
    println!("💅 SlayGurl Rust Compiler V 1.00");
    println!("Initializing Rust Optimiazations...");

    let time_saved_by_the_superior_language_that_is_rust = rand::random_range(0..30);

    std::thread::sleep(Duration::from_secs(time_saved_by_the_superior_language_that_is_rust));

    
    let a:String = std::process::Command::new("./src/SGC.exe")
                                                                                            .arg(args[0].clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone())
                                                                                                .output()
                                                                                                    .unwrap()
                                                                                                        .stdout
                                                                                                                .iter()
                                                                                                                    .map(|x| *x as char)
                                                                                                                        .collect::<String>();


    println!("\n\n");
    println!("Finished Compiling {}. Rust Optimizations saved {} seconds", args[0].clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone().clone(),time_saved_by_the_superior_language_that_is_rust);
    println!("\n\n");
    print!("{a:?}");

}
